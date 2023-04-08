"""Define dependencies serializers."""
from typing import List

from rest_framework import serializers

from core.models import Dependency, Ingest, Project


class ProjectSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=Project.NAME_LENGTH)

    def create(self, validated_data) -> Project:
        project, _ = Project.objects.get_or_create(name=validated_data["name"])
        return project


class IngestDependencySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=Dependency.NAME_LENGTH)
    version = serializers.CharField(max_length=Dependency.VERSION_LENGTH)

    def create(self, validated_data) -> Dependency():
        try:
            dependency = Dependency.objects.filter(
                name=self.validated_data["name"],
                version=validated_data["version"],
            ).get()
        except Dependency.DoesNotExist:
            dependency = Dependency(
                name=validated_data["name"], version=validated_data["version"], ecosystem=self.context.get("ecosystem")
            )
            dependency.save()
        return dependency


class NewIngestSerializer(serializers.Serializer):
    hash_id = serializers.CharField(max_length=Ingest.HASH_ID_LENGTH)
    ecosystem = serializers.ChoiceField(choices=Ingest.ECOSYSTEM_CHOICES)
    dependencies = serializers.ListSerializer(child=IngestDependencySerializer())

    def create(self, validated_data) -> Ingest:
        try:
            ingest = Ingest.objects.get(hash_id=validated_data["hash_id"])
        except Ingest.DoesNotExist:
            ingest = Ingest(
                hash_id=validated_data["hash_id"],
                ecosystem=validated_data["ecosystem"],
                project=self.context.get("project"),
            )

            for dependency in ingest.project.dependencies.all():
                if dependency.ecosystem == ingest.ecosystem:
                    ingest.project.dependencies.remove(dependency)
                    if not dependency.projects.all():
                        dependency.delete()
            ingest.save()

            dependencies_data = self.validated_data["dependencies"]
            for dependency_data in dependencies_data:
                dependency_serializer = IngestDependencySerializer(
                    data=dependency_data, context={"ecosystem": validated_data["ecosystem"]}
                )
                dependency_serializer.is_valid(raise_exception=True)
                dependency = dependency_serializer.save()
                dependency.assign_ingest(ingest)

                ingest.dependencies.add(dependency)
                ingest.project.dependencies.add(dependency)
        return ingest


class RequestIngestSerializer(serializers.Serializer):
    project = ProjectSerializer()
    ingests = serializers.ListSerializer(child=NewIngestSerializer())

    def create(self, validated_data) -> List[Ingest]:
        project_serializer = ProjectSerializer(data=self.validated_data["project"])
        project_serializer.is_valid(raise_exception=True)
        project = project_serializer.save()

        ingests = []
        ingests_data = validated_data["ingests"]
        for ingest_data in ingests_data:
            ingest_serializer = NewIngestSerializer(data=ingest_data, context={"project": project})
            ingest_serializer.is_valid(raise_exception=True)
            ingests.append(ingest_serializer.save())
        return ingests
