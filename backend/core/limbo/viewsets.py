from rest_framework import viewsets

from core.models import Dependecy
from core.serializers import DependencySerializer


class DependencyViewSet(viewsets.ModelViewSet):
    queryset = Dependecy.objects.all()
    serializer_class = DependencySerializer
