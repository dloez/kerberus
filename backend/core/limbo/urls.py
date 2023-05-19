from django.urls import path

from core.limbo import views

urlpatterns = [
    path("ingest/", views.ingest_dependencies, name="ingest"),
    path("vulnerabilities/update", views.update_vulnerabilities, name="update_vulnerabilities"),
    path("projects/summary", views.get_projects_summaries, name="projects"),
    path("projects/<int:id>/dependencies", views.get_project_dependencies, name="project_dependencies"),
    path("projects/<int:id>/vulnerabilities", views.get_project_vulnerabilities, name="project_vulnerabilities"),
    path(
        "projects/<int:project_id>/dependencies/<int:dependency_id>/vulnerabilities",
        views.get_project_dependency_vulnerabilities,
        name="project_dependency_vulnerabilities",
    ),
    path(
        "projects/<int:project_id>/vulnerabilities/<str:vulnerability_id>",
        views.get_project_vulnerability,
        name="project_vulnerability",
    ),
]
