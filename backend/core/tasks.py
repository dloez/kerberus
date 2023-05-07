from itertools import zip_longest

import requests
from django.conf import settings
from django.core.paginator import Page, Paginator
from huey.contrib.djhuey import task

from core.models import Dependency, Project, Vulnerability, VulnerabilityDependency


def grouper(iterable, chunk_size, fillvalue=None):
    args = [iter(iterable)] * chunk_size
    return zip_longest(*args, fillvalue=fillvalue)


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
            if "vulns" not in dependency_vulnerabilities:
                continue
            dependency_vulnerabilities = dependency_vulnerabilities["vulns"]
            for vulnerability in dependency_vulnerabilities:
                try:
                    dependency.vulnerabilities.get(osv_id=vulnerability["id"])
                except Vulnerability.DoesNotExist:
                    try:
                        Vulnerability.objects.get(osv_id=vulnerability["id"])
                    except Vulnerability.DoesNotExist:
                        osv_depencency_vulnerability = osv_get_vulnerability(vulnerability["id"])
                        create_vulnerability(osv_depencency_vulnerability, dependency)


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

    relationship = VulnerabilityDependency(vulnerability=vulnerability, dependency=dependency, fixed_versions=[])
    relationship.save()
    return vulnerability
