from django.urls import path

from core.limbo import views

urlpatterns = [
    path("ingest/", views.ingest_dependencies, name="ingest"),
    path("vulnerabilities/update", views.update_vulnerabilities, name="update_vulnerabilities"),
    path("projects/summary", views.get_projects_summaries, name="projects"),
    path("projects/<int:id>/dependencies", views.get_project_dependencies, name="project_dependencies"),
    path("projects/<int:id>/vulnerabilities", views.get_project_vulnerabilities, name="project_vulnerabilities"),
]
