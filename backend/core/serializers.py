"""Define dependencies serializers."""
from rest_framework import serializers

from core.models import Dependecy


class DependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependecy
        fields = "__all__"
