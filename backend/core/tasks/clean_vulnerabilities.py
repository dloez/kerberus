from huey.contrib.djhuey import db_task, lock_task

from core.models import Vulnerability


@db_task()
@lock_task("clean_vulns")
def clean_vulnerabilities():
    vulnerabilities = Vulnerability.objects.all()
    for vulnerability in vulnerabilities:
        if not vulnerability.vulnerabilitydependency_set.exists():
            vulnerability.delete()
