"""Define core functionalities models."""
from django.db import models


class Dependecy(models.Model):
    """Define Dependency model to represent project dependencies."""

    package_name = models.CharField(max_length=100)
    version = models.CharField(max_length=100)
