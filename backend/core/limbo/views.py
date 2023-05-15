"""Limbo REST-API version views."""
from django.http import Http404
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Dependency, Ingest, Project
from core.serializers import RequestIngestSerializer
from core.tasks import collect_vulnerabilities


@api_view(["POST"])
def ingest_dependencies(request):
    """Create and store dependencies from the given ingest"""

    request_ingests = RequestIngestSerializer(data=request.data)
    if not request_ingests.is_valid():
        return Response({"status": "failed to digest ingest", "errors": request_ingests.error_messages})
    request_ingests.save()
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
def get_project_dependencies(request, id):
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
    collect_vulnerabilities()
    return Response(status=status.HTTP_200_OK)
