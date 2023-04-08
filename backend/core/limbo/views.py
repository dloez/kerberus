"""Limbo REST-API version views."""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.serializers import RequestIngestSerializer


@api_view(["POST"])
def ingest_dependencies(request):
    """Create and store dependencies from the given ingest"""

    request_ingests = RequestIngestSerializer(data=request.data)
    if not request_ingests.is_valid():
        return Response({"status": "failed to digest ingest", "errors": request_ingests.error_messages})
    request_ingests.save()
    return Response(status=status.HTTP_201_CREATED)
