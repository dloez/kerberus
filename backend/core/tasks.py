from statistics import mean

import requests
from cvss import CVSS2, CVSS3
from django.conf import settings
from django.core.paginator import Page, Paginator
from huey.contrib.djhuey import task

from core.models import Dependency, Project, Vulnerability, VulnerabilityDependency


@task()
def collect_vulnerabilities(project_id=None):
    if not project_id:
        dependencies = Dependency.objects.all().order_by("id")
    else:
        try:
            project = Project.objects.get(id=project_id)
            dependencies = project.dependencies
        except Project.DoesNotExist:
            return

    paginator = Paginator(dependencies, 100)
    for page_num in paginator.page_range:
        page = paginator.page(page_num)
        vulnerabilities = osv_get_vulnerabilities_batch(page)
        for dependency, dependency_vulnerabilities in zip(page, vulnerabilities):
            dependency.vulnerabilitydependency_set.all().delete()
            if "vulns" not in dependency_vulnerabilities:
                continue

            dependency_vulnerabilities = dependency_vulnerabilities["vulns"]
            for osv_vulnerability in dependency_vulnerabilities:
                try:
                    vulnerability = Vulnerability.objects.get(osv_id=osv_vulnerability["id"])
                    osv_vulnerability = osv_get_vulnerability(osv_vulnerability["id"])
                    update_vulnerability_fields(vulnerability, osv_vulnerability, auto_save=True)
                    fixed_versions = get_vulnerability_fixed_versions(osv_vulnerability, dependency)
                    vulnerability_dependency = VulnerabilityDependency(
                        dependency=dependency, vulnerability=vulnerability, fixed_versions=fixed_versions
                    )
                    vulnerability_dependency.save()
                except Vulnerability.DoesNotExist:
                    osv_vulnerability = osv_get_vulnerability(osv_vulnerability["id"])
                    vulnerability = create_vulnerability(osv_vulnerability, dependency)


def osv_get_vulnerabilities_batch(dependencies: Page) -> dict:
    osv_batch = {"queries": []}
    for dependency in dependencies:
        dep_request = {
            "package": {"ecosystem": dependency.ecosystem.capitalize(), "name": dependency.name},
            "version": dependency.version,
        }
        osv_batch["queries"].append(dep_request)
    r = requests.post(settings.OSV_QUERY_BATCH_URL, json=osv_batch)
    return r.json()["results"]


def osv_get_vulnerability(id: str) -> dict:
    return requests.get(settings.OSV_GET_VULN_URL.format(id)).json()


def create_vulnerability(osv_vulnerability: dict, dependency: Dependency) -> Vulnerability:
    cve_id = osv_vulnerability["aliases"][0]
    vulnerability = Vulnerability(
        osv_id=osv_vulnerability["id"],
        cve_id=cve_id,
    )
    update_vulnerability_fields(vulnerability, osv_vulnerability, auto_save=True)

    fixed_versions = get_vulnerability_fixed_versions(osv_vulnerability, dependency)
    relationship = VulnerabilityDependency(
        vulnerability=vulnerability, dependency=dependency, fixed_versions=fixed_versions
    )
    relationship.save()
    return vulnerability


def get_vulnerability_fixed_versions(osv_vulnerability: dict, dependency: Dependency) -> list[str] | None:
    for affected_package in osv_vulnerability["affected"]:
        if affected_package["package"]["name"] != dependency.name:
            continue
        if affected_package["package"]["ecosystem"] != dependency.ecosystem.capitalize():
            continue
        if dependency.version not in affected_package["versions"]:
            continue

        fixed_versions = []
        for affected_range in affected_package["ranges"]:
            for event in affected_range["events"]:
                if "fixed" in event:
                    fixed_versions.append(event["fixed"])
        return fixed_versions
    return []


def get_vulnerability_severity_fields(osv_vulnerability) -> ():
    severities = osv_vulnerability["severity"]

    cvss = [severity for severity in severities if severity["type"] == "CVSS_V3"]
    if not cvss:
        cvss = [severity for severity in severities if severity["type"] == "CVSS_V2"]
    if not cvss:
        return "", 0.0, "", 0.0, "", 0.0, "", 0.0, ""

    cvss_objs = {"CVSS_V3": CVSS3, "CVSS_V2": CVSS2}

    cvss = cvss[0]
    severity = cvss["score"]
    cvss = cvss_objs[cvss["type"]](cvss["score"])

    base_score, temporal_score, environmental_score = cvss.scores()
    base_score_string, temporal_score_string, environmental_score_string = cvss.severities()

    overall_score = mean((base_score, temporal_score, environmental_score))
    if overall_score == 0.0:
        overall_score_string = Vulnerability.NONE
    elif 0.1 <= overall_score <= 3.9:
        overall_score = Vulnerability.LOW
    elif 4.0 <= overall_score <= 6.9:
        overall_score_string = Vulnerability.MEDIUM
    elif 7.0 <= overall_score <= 8.9:
        overall_score_string = Vulnerability.HIGH
    else:
        overall_score_string = Vulnerability.CRITICAL
    return (
        severity,
        base_score,
        base_score_string.upper(),
        temporal_score,
        temporal_score_string.upper(),
        environmental_score,
        environmental_score_string.upper(),
        overall_score,
        overall_score_string,
    )


def update_vulnerability_fields(vulnerability: Vulnerability, osv_vulnerability: dict, auto_save: bool = False):
    (
        severity,
        base_score,
        base_score_string,
        temporal_score,
        temporal_score_string,
        environmental_score,
        environmental_score_string,
        overall_score,
        overall_score_string,
    ) = get_vulnerability_severity_fields(osv_vulnerability)
    if severity == vulnerability.severity:
        return

    vulnerability.severity = severity
    vulnerability.severity_base_score = base_score
    vulnerability.severity_base_score_string = base_score_string
    vulnerability.severity_temporal_score = temporal_score
    vulnerability.severity_temporal_score_string = temporal_score_string
    vulnerability.severity_environmental_score = environmental_score
    vulnerability.severity_environmental_score_string = environmental_score_string
    vulnerability.severity_overall_score = overall_score
    vulnerability.severity_overall_score_string = overall_score_string
    if auto_save:
        vulnerability.save()
