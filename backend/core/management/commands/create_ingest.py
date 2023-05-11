import random
from hashlib import sha256

from django.core.management.base import BaseCommand

from core.models import Dependency, Ingest, Project


class Command(BaseCommand):
    help = "Create ingest with the given amount of dependencies"

    def add_arguments(self, parser):
        parser.add_argument("project_name", type=str)

        parser.add_argument(
            "--dependencies", help="Amount of dependencies that the Ingest should add", default=100, type=int
        )

    def handle(self, *args, **options):
        dependencies = options["dependencies"]
        if dependencies < 3:
            dependencies = 3
            print("minimum amount of dependencies is 3...")

        project = Project.objects.filter(name=options["project_name"]).first()
        ecosystem = random.choice(Ingest.ECOSYSTEM_CHOICES)[0]
        ingest = Ingest(hash_id=get_random_hash_hexstring(), ecosystem=ecosystem, project=project)
        ingest.save()

        # hardcoded real dependencies with vulnerabilities
        if ecosystem in REAL_DEPENDENCIES:
            vulns = REAL_DEPENDENCIES[ecosystem]
            for vuln in vulns:
                name, version = vuln.split("@")
                dependency = Dependency(name=name, version=version, ecosystem=ecosystem, ingest=ingest)
                dependency.save()
                dependencies -= 1

        for i in range(dependencies):
            create_dependency(ingest, ecosystem)


def create_dependency(ingest: Ingest, ecosystem: str):
    name = ""
    version = ""
    for i in range(3):
        name += random.choice(WORDS).capitalize()
        version += str(random.randint(0, 9)) + "."
    version = version[:-1]

    dependency = Dependency(name=name, version=version, ecosystem=ecosystem, ingest=ingest)
    dependency.save()


def get_random_hash_hexstring() -> str:
    random_data = random.getrandbits(128)
    return sha256(str(random_data).encode("utf-8")).hexdigest()


WORDS = [
    "apple",
    "banana",
    "orange",
    "grape",
    "kiwi",
    "lemon",
    "lime",
    "mango",
    "peach",
    "pear",
    "pineapple",
    "strawberry",
    "watermelon",
    "blueberry",
    "raspberry",
    "blackberry",
    "cherry",
    "coconut",
    "pomegranate",
    "apricot",
    "fig",
    "guava",
    "plum",
    "tangerine",
    "cantaloupe",
    "honeydew",
    "nectarine",
    "papaya",
    "persimmon",
    "quince",
    "avocado",
    "jackfruit",
    "durian",
    "dragonfruit",
    "starfruit",
    "passionfruit",
    "lychee",
    "mulberry",
    "boysenberry",
    "elderberry",
    "gooseberry",
    "cranberry",
    "kumquat",
    "rhubarb",
    "tomato",
    "eggplant",
    "cucumber",
    "carrot",
    "broccoli",
]

REAL_DEPENDENCIES = {
    "maven": [
        "org.xwiki.commons:xwiki-commons-xml@14.10",
        "org.testng:testng@6.13",
        "org.apache.ranger:ranger-hive-plugin@2.0.0",
    ],
    "npm": ["uap-core@0.1.0", "http-cache-semantics@3.8.1", "uglify-js@0.1.0"],
}
