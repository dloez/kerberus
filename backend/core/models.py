"""Define core functionalities models."""
from django.db import models


class Project(models.Model):
    """Define Project model."""

    NAME_LENGTH: int = 100

    name = models.CharField(max_length=NAME_LENGTH, primary_key=True)
    dependencies = models.ManyToManyField("Dependency", related_name="projects")


class Ingest(models.Model):
    """Define Ingest model to represent when a user posts dependencies from a project."""

    HASH_ID_LENGTH: int = 64

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    hash_id = models.CharField(max_length=HASH_ID_LENGTH, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    dependencies = models.ManyToManyField("Dependency", related_name="ingests")


class Dependency(models.Model):
    """Define Dependency model to represent project dependencies."""

    PACKAGE_NAME_LENGTH: int = 100
    VERSION_LENGTH: int = 20

    package_name = models.CharField(max_length=PACKAGE_NAME_LENGTH, primary_key=True)
    version = models.CharField(max_length=VERSION_LENGTH)
    ingest = models.ForeignKey(Ingest, on_delete=models.SET_NULL, null=True)

    def assign_ingest(self, ingest: Ingest):
        if self.ingest:
            return

        self.ingest = ingest
        self.save()
