from django.core.management.base import BaseCommand

from core.models import Project


class Command(BaseCommand):
    help = "Create a project with the given name"

    def add_arguments(self, parser):
        parser.add_argument("name", type=str)

    def handle(self, *args, **options):
        project = Project(name=options["name"])
        project.save()
