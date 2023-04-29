from django.urls import path

from core.limbo import views

urlpatterns = [
    path("ingest/", views.ingest_dependencies, name="ingest"),
    path("projects/summary", views.get_projects_summaries, name="projects"),
]
