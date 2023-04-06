"""Define dependencies serializers."""
from rest_framework import serializers

from core.models import Dependency, Ingest, Project


class IngestDependencySerializer(serializers.Serializer):
    package_name = serializers.CharField(max_length=Dependency.PACKAGE_NAME_LENGTH)
    version = serializers.CharField(max_length=Dependency.VERSION_LENGTH)

    def create(self):
        try:
            dependency = Dependency.objects.filter(
                package_name=self.validated_data["package_name"], version=self.validated_data["version"]
            ).get()
        except Dependency.DoesNotExist:
            dependency = Dependency(
                package_name=self.validated_data["package_name"], version=self.validated_data["version"]
            )
            dependency.save()
        return dependency


class IngestDependencyListSerializer(serializers.ListSerializer):
    child = IngestDependencySerializer()


class RawIngestSerializer(serializers.Serializer):
    hash_id = serializers.CharField(max_length=Ingest.HASH_ID_LENGTH)
    dependencies = serializers.ListSerializer(child=IngestDependencySerializer())
    project = serializers.CharField(max_length=Project.NAME_LENGTH)

    def validate_project(self, value):
        try:
            Project.objects.get(name=value)
        except Project.DoesNotExist:
            raise serializers.ValidationError(f"Project with name '{value}' does not exist")
        return value

    def create(self):
        project = Project.objects.get(name=self.validated_data["project"])

        try:
            ingest = Ingest.objects.get(hash_id=self.validated_data["hash_id"])
        except Ingest.DoesNotExist:
            ingest = Ingest(hash_id=self.validated_data["hash_id"], project=project)
            ingest.save()

            dependencies_data = self.validated_data["dependencies"]
            for dependency_data in dependencies_data:
                dependency_serializer = IngestDependencySerializer(data=dependency_data)
                dependency_serializer.is_valid(raise_exception=True)
                new_dependency = dependency_serializer.create()
                new_dependency.assign_ingest(ingest)

                ingest.dependencies.add(new_dependency)
                project.dependencies.add(new_dependency)
        return ingest
