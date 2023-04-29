"""Limbo REST-API version views."""
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Project
from core.serializers import RequestIngestSerializer


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
        name = serializers.CharField(max_length=Project.NAME_LENGTH)

    from_element = int(request.query_params.get("from", 0))
    to_element = int(request.query_params.get("to", 10))
    projects = Project.objects.all()[from_element:to_element].only("name")
    project_serializer = ProjectSerializer(projects, many=True)
    return Response(project_serializer.data, status=status.HTTP_200_OK)
