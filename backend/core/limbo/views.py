"""Limbo REST-API version views."""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.serializers import RawIngestSerializer


@api_view(["POST"])
def ingest_dependencies(request):
    """Create and store dependencies from the given ingest"""

    ingest = RawIngestSerializer(data=request.data)
    if not ingest.is_valid():
        return Response({"status": "failed to digest ingest", "errors": ingest.error_messages})
    ingest.create()
    return Response(status=status.HTTP_201_CREATED)
