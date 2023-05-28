"""Limbo REST-API version views."""
from django.http import Http404
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.collect_vulnerabilities import collect_vulnerabilities
from core.models import Dependency, Ingest, Project, Vulnerability, VulnerabilityDependency
from core.serializers import RequestIngestSerializer


@api_view(["POST"])
def ingest_dependencies(request):
    """Create and store dependencies from the given ingest"""

    request_ingests = RequestIngestSerializer(data=request.data)
    if not request_ingests.is_valid():
        return Response({"status": "failed to digest ingest", "errors": request_ingests.error_messages})
    request_ingests.save()
    collect_vulnerabilities()()
    return Response(status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_projects_summaries(request):
    class ProjectSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField(max_length=Project.NAME_LENGTH)

    from_element = int(request.query_params.get("from", 0))
    to_element = int(request.query_params.get("to", 10))
    projects = Project.objects.all()[from_element:to_element].only("name")
    project_serializer = ProjectSerializer(projects, many=True)
    return Response(project_serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_project_dependencies(request, id: int):
    class DependencySerializer(serializers.Serializer):
        name = serializers.CharField(max_length=Dependency.NAME_LENGTH)
        version = serializers.CharField(max_length=Dependency.VERSION_LENGTH)
        ecosystem = serializers.ChoiceField(choices=Ingest.ECOSYSTEM_CHOICES)
        total_vulnerabilities = serializers.IntegerField()
        total_vulnerabilities_low = serializers.IntegerField()
        total_vulnerabilities_medium = serializers.IntegerField()
        total_vulnerabilities_high = serializers.IntegerField()
        total_vulnerabilities_critical = serializers.IntegerField()

    try:
        project = Project.objects.get(id=id)
    except Project.DoesNotExist:
        raise Http404(f"Project with id '{id}' does not exist")

    from_element = int(request.query_params.get("from", 0))
    to_element = int(request.query_params.get("to", 10))
    dependencies = project.dependencies.all()[from_element:to_element].only("name")
    dependencies_serializer = DependencySerializer(dependencies, many=True)
    return Response(dependencies_serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
def update_vulnerabilities(request, pk=None):
    collect_vulnerabilities()()
    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def get_project_vulnerabilities(request, id: int):
    class VulnerabilitySerializer(serializers.Serializer):
        osv_id = serializers.CharField(max_length=Vulnerability.OSV_ID_LENGTH)
        cve_id = serializers.CharField(max_length=Vulnerability.CVE_ID_LENGTH)
        severity_overall_score = serializers.FloatField()
        severity_overall_score_string = serializers.ChoiceField(choices=Vulnerability.SEVERITY_SCORE_STRING_CHOICES)
        fix_available = serializers.BooleanField()

    try:
        project = Project.objects.get(id=id)
    except Project.DoesNotExist:
        raise Http404(f"Project with id '{id}' does not exist")

    from_element = int(request.query_params.get("from", 0))
    to_element = int(request.query_params.get("to", 10))
    vulnerabilities = Vulnerability.objects.filter(dependencies__projects=project)[from_element:to_element]
    res_vulnerabilities = []
    for vulnerability in vulnerabilities:
        fix_available = bool(
            VulnerabilityDependency.objects.filter(vulnerability=vulnerability).exclude(fixed_versions__exact="[]")
        )
        vulnerability = {
            "osv_id": vulnerability.osv_id,
            "cve_id": vulnerability.cve_id,
            "severity_overall_score": vulnerability.severity_overall_score,
            "severity_overall_score_string": vulnerability.severity_overall_score_string,
            "fix_available": fix_available,
        }
        res_vulnerabilities.append(vulnerability)
    serializer = VulnerabilitySerializer(res_vulnerabilities, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_project_dependency_vulnerabilities(request, project_id: int, dependency_id: int):
    class VulnerabilitySerializer(serializers.Serializer):
        osv_id = serializers.CharField(max_length=Vulnerability.OSV_ID_LENGTH)
        cve_id = serializers.CharField(max_length=Vulnerability.CVE_ID_LENGTH)
        severity_overall_score = serializers.FloatField()
        severity_overall_score_string = serializers.ChoiceField(choices=Vulnerability.SEVERITY_SCORE_STRING_CHOICES)
        fixed_versions = serializers.ListField()

    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        raise Http404(f"Project with id '{project_id}' does not exist")

    try:
        dependency = project.dependencies.get(id=dependency_id)
    except Project.DoesNotExist:
        raise Http404(f"Dependency with id '{dependency_id}' does not exist")

    from_element = int(request.query_params.get("from", 0))
    to_element = int(request.query_params.get("to", 10))
    vulnerabilities = dependency.vulnerabilities.all()[from_element:to_element]
    res_vulnerabilities = []
    for vulnerability in vulnerabilities:
        vulnerability = {
            "osv_id": vulnerability.osv_id,
            "cve_id": vulnerability.cve_id,
            "severity_overall_score": vulnerability.severity_overall_score,
            "severity_overall_score_string": vulnerability.severity_overall_score_string,
            "fixed_versions": VulnerabilityDependency.objects.filter(
                vulnerability=vulnerability, dependency=dependency
            )
            .first()
            .get_fixed_versions(),
        }
        res_vulnerabilities.append(vulnerability)
    serializer = VulnerabilitySerializer(res_vulnerabilities, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_project_vulnerability(request, project_id: int, vulnerability_id: str):
    class AffectedDependencySerializer(serializers.Serializer):
        name = serializers.CharField(max_length=Dependency.NAME_LENGTH)
        version = serializers.CharField(max_length=Dependency.VERSION_LENGTH)
        ecosystem = serializers.ChoiceField(choices=Ingest.ECOSYSTEM_CHOICES)
        fixed_versions = serializers.ListField()

    class VulnerabilitySerializer(serializers.Serializer):
        osv_id = serializers.CharField(max_length=Vulnerability.OSV_ID_LENGTH)
        cve_id = serializers.CharField(max_length=Vulnerability.CVE_ID_LENGTH)
        severity_overall_score = serializers.FloatField()
        severity_overall_score_string = serializers.ChoiceField(choices=Vulnerability.SEVERITY_SCORE_STRING_CHOICES)
        affected_project_dependencies = serializers.ListSerializer(child=AffectedDependencySerializer())

    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        raise Http404(f"Project with id '{project_id}' does not exist")

    try:
        vulnerability = Vulnerability.objects.get(osv_id=vulnerability_id)
    except Project.DoesNotExist:
        raise Http404(f"Vulnerability with id '{vulnerability_id}' does not exist")

    from_element = int(request.query_params.get("from", 0))
    to_element = int(request.query_params.get("to", 10))
    affected_project_vulnerability_dependency = VulnerabilityDependency.objects.filter(
        dependency__projects=project, vulnerability=vulnerability
    ).all()[from_element:to_element]

    vulnerability_dependencies = []
    for vulnerability_dependency in affected_project_vulnerability_dependency:
        vulnerability_dependency = {
            "name": vulnerability_dependency.dependency.name,
            "version": vulnerability_dependency.dependency.version,
            "ecosystem": vulnerability_dependency.dependency.ecosystem,
            "fixed_versions": vulnerability_dependency.get_fixed_versions(),
        }
        vulnerability_dependencies.append(vulnerability_dependency)
    vulnerability = {
        "osv_id": vulnerability.osv_id,
        "cve_id": vulnerability.cve_id,
        "severity_overall_score": vulnerability.severity_overall_score,
        "severity_overall_score_string": vulnerability.severity_overall_score_string,
        "affected_project_dependencies": vulnerability_dependencies,
    }
    serializer = VulnerabilitySerializer(vulnerability)
    return Response(serializer.data, status=status.HTTP_200_OK)
