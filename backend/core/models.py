"""Define core functionalities models."""
import json

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
    vulnerabilities = models.ManyToManyField(
        "Vulnerability", through="VulnerabilityDependency", related_name="dependencies"
    )

    total_vulnerabilities = models.IntegerField(default=0)
    total_vulnerabilities_low = models.IntegerField(default=0)
    total_vulnerabilities_medium = models.IntegerField(default=0)
    total_vulnerabilities_high = models.IntegerField(default=0)
    total_vulnerabilities_critical = models.IntegerField(default=0)

    def assign_ingest(self, ingest: Ingest):
        if self.ingest:
            self.ingests.add(ingest)
            return

        self.ingests.add(ingest)
        self.ingest = ingest
        self.save()


class Vulnerability(models.Model):
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    SEVERITY_SCORE_STRING_CHOICES = ((NONE, NONE), (LOW, LOW), (MEDIUM, MEDIUM), (HIGH, HIGH), (CRITICAL, CRITICAL))

    OSV_ID_LENGTH = 100
    CVE_ID_LENGTH = 100
    SEVERITY_LENGTH = 100

    osv_id = models.CharField(max_length=OSV_ID_LENGTH, primary_key=True)
    cve_id = models.CharField(max_length=CVE_ID_LENGTH, null=True)
    severity = models.CharField(max_length=SEVERITY_LENGTH, null=True)
    severity_base_score = models.FloatField(null=True)
    severity_base_score_string = models.CharField(max_length=8, choices=SEVERITY_SCORE_STRING_CHOICES, null=True)
    severity_temporal_score = models.FloatField(null=True)
    severity_temporal_score_string = models.CharField(max_length=8, choices=SEVERITY_SCORE_STRING_CHOICES, null=True)
    severity_environmental_score = models.FloatField(null=True)
    severity_environmental_score_string = models.CharField(
        max_length=8, choices=SEVERITY_SCORE_STRING_CHOICES, null=True
    )
    severity_overall_score = models.FloatField(null=True)
    severity_overall_score_string = models.CharField(max_length=8, choices=SEVERITY_SCORE_STRING_CHOICES, null=True)
    last_updated = models.DateTimeField(auto_now=True)


class VulnerabilityDependency(models.Model):
    dependency = models.ForeignKey("Dependency", on_delete=models.CASCADE)
    vulnerability = models.ForeignKey("Vulnerability", on_delete=models.CASCADE)
    fixed_versions = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if isinstance(self.fixed_versions, list):
            self.fixed_versions = json.dumps(self.fixed_versions)
        super().save(*args, **kwargs)
