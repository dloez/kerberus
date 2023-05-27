import re
from statistics import mean

import requests
from cvss import CVSS2, CVSS3
from django.conf import settings
from django.core.paginator import Page, Paginator
from huey.contrib.djhuey import task
from packaging.version import parse as parse_version

from core.models import Dependency, Ingest, Project, Vulnerability, VulnerabilityDependency


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
                    create_update_vulnerability_and_dependency(
                        osv_vulnerability, dependency, vulnerability=vulnerability
                    )
                except Vulnerability.DoesNotExist:
                    osv_vulnerability = osv_get_vulnerability(osv_vulnerability["id"])
                    create_update_vulnerability_and_dependency(osv_vulnerability, dependency)
            populate_vulnerabilities_in_dependency(dependency)


def osv_get_vulnerabilities_batch(dependencies: Page) -> dict:
    osv_batch = {"queries": []}
    for dependency in dependencies:
        dep_request = {
            "package": {"ecosystem": OSV_ECOSYSTEM_NAMES[dependency.ecosystem], "name": dependency.name},
            "version": dependency.version,
        }
        osv_batch["queries"].append(dep_request)
    r = requests.post(settings.OSV_QUERY_BATCH_URL, json=osv_batch)
    return r.json()["results"]


def osv_get_vulnerability(id: str) -> dict:
    return requests.get(settings.OSV_GET_VULN_URL.format(id)).json()


def create_update_vulnerability_and_dependency(
    osv_vulnerability: dict, dependency: Dependency, vulnerability: Vulnerability = None
) -> Vulnerability:
    if not vulnerability:
        vulnerability = Vulnerability(osv_id=osv_vulnerability["id"])

    changed = False
    cve_id = osv_vulnerability["aliases"][0]  # TODO: check scheme and add validations
    if cve_id != vulnerability.cve_id:
        vulnerability.cve_id = cve_id
        changed = True

    severities_changed = update_vulnerability_severity_fields(vulnerability, osv_vulnerability)
    if severities_changed and not changed:
        changed = True

    if changed:
        vulnerability.save()

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
        if affected_package["package"]["ecosystem"] != OSV_ECOSYSTEM_NAMES[dependency.ecosystem]:
            continue

        fixed_versions = []
        for affected_range in affected_package["ranges"]:
            introduced = ""
            fixed = ""
            for event in affected_range["events"]:
                if "introduced" in event:
                    introduced = event["introduced"]
                if "fixed" in event:
                    fixed = event["fixed"]

            if not fixed:
                continue

            if affected_range["type"] == RANGE_ECOSYSTEM:
                if dependency.version in affected_package["versions"]:
                    fixed_versions.append(fixed)
                continue

            if affected_range["type"] == RANGE_SEMVER:
                parsed_introduced = parse_version(introduced)
                parsed_fixed = parse_version(fixed)
                parsed_dependency_version = parse_version(re.sub("[^0-9.]", "", dependency.version))
                if parsed_introduced <= parsed_dependency_version <= parsed_fixed:
                    fixed_versions.append(fixed)
        return fixed_versions
    return []


def get_osv_vulnerability_severity_fields(osv_vulnerability) -> ():
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

    overall_score = round(mean((base_score, temporal_score, environmental_score)), 1)
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


def update_vulnerability_severity_fields(vulnerability: Vulnerability, osv_vulnerability: dict) -> bool:
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
    ) = get_osv_vulnerability_severity_fields(osv_vulnerability)
    if severity == vulnerability.severity:
        return False

    vulnerability.severity = severity
    vulnerability.severity_base_score = base_score
    vulnerability.severity_base_score_string = base_score_string
    vulnerability.severity_temporal_score = temporal_score
    vulnerability.severity_temporal_score_string = temporal_score_string
    vulnerability.severity_environmental_score = environmental_score
    vulnerability.severity_environmental_score_string = environmental_score_string
    vulnerability.severity_overall_score = overall_score
    vulnerability.severity_overall_score_string = overall_score_string
    return True


def populate_vulnerabilities_in_dependency(dependency: Dependency):
    total_vulnerabilities = {
        Vulnerability.NONE: 0,
        Vulnerability.LOW: 0,
        Vulnerability.MEDIUM: 0,
        Vulnerability.HIGH: 0,
        Vulnerability.CRITICAL: 0,
    }
    for vulnerability in dependency.vulnerabilities.all():
        total_vulnerabilities[vulnerability.severity_overall_score_string] += 1
    total_vulnerabilities[Vulnerability.LOW] = sum(
        (total_vulnerabilities[Vulnerability.LOW], total_vulnerabilities[Vulnerability.NONE])
    )
    all_vulnerabilities = sum(total_vulnerabilities.values())

    dirty_fields = set()
    dirty_fields.add(change_attr(total_vulnerabilities[Vulnerability.LOW], "total_vulnerabilities_low", dependency))
    dirty_fields.add(
        change_attr(total_vulnerabilities[Vulnerability.MEDIUM], "total_vulnerabilities_medium", dependency)
    )
    dirty_fields.add(change_attr(total_vulnerabilities[Vulnerability.HIGH], "total_vulnerabilities_high", dependency))
    dirty_fields.add(
        change_attr(total_vulnerabilities[Vulnerability.CRITICAL], "total_vulnerabilities_critical", dependency)
    )
    dirty_fields.add(change_attr(all_vulnerabilities, "total_vulnerabilities", dependency))
    dirty_fields.remove("")
    if dirty_fields:
        dependency.save(update_fields=dirty_fields)


def change_attr(attr_value, attr_name: str, obj) -> str:
    if attr_value != getattr(obj, attr_name):
        setattr(obj, attr_name, attr_value)
        return attr_name
    return ""


OSV_ECOSYSTEM_NAMES = {Ingest.MAVEN: "Maven", Ingest.NPM: "npm"}
RANGE_ECOSYSTEM = "ECOSYSTEM"
RANGE_SEMVER = "SEMVER"
