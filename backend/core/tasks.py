import requests
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
    vulnerability = Vulnerability(osv_id=osv_vulnerability["id"], cve_id=cve_id)
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
