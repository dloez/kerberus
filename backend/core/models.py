"""Define core functionalities models."""
from django.db import models


class Project(models.Model):
    """Define Project model."""

    NAME_LENGTH: int = 100

    name = models.CharField(max_length=NAME_LENGTH)
    dependencies = models.ManyToManyField("Dependency", related_name="projects")


class Ingest(models.Model):
    """Define Ingest model to represent when a user posts dependencies from a project."""

    HASH_ID_LENGTH: int = 64

    MAVEN = "maven"
    NPM = "npm"
    ECOSYSTEM_CHOICES = ((MAVEN, "maven"), (NPM, "npm"))

    hash_id = models.CharField(max_length=HASH_ID_LENGTH, primary_key=True)
    ecosystem = models.CharField(max_length=10, choices=ECOSYSTEM_CHOICES)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    dependencies = models.ManyToManyField("Dependency", related_name="ingests")


class Dependency(models.Model):
    """Define Dependency model to represent project dependencies."""

    NAME_LENGTH: int = 100
    VERSION_LENGTH: int = 20

    name = models.CharField(max_length=NAME_LENGTH)
    version = models.CharField(max_length=VERSION_LENGTH)
    ingest = models.ForeignKey("Ingest", on_delete=models.SET_NULL, null=True)
    ecosystem = models.CharField(max_length=10, choices=Ingest.ECOSYSTEM_CHOICES)

    def assign_ingest(self, ingest: Ingest):
        if self.ingest:
            self.ingests.add(ingest)
            return

        self.ingests.add(ingest)
        self.ingest = ingest
        self.save()
