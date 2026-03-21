from django.urls import path

from .views import ProjectDetailView, ProjectDocumentCreateView, ProjectListCreateView


urlpatterns = [
    path("", ProjectListCreateView.as_view(), name="project-list"),
    path("<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("<int:project_id>/documents/", ProjectDocumentCreateView.as_view(), name="project-document-create"),
]
