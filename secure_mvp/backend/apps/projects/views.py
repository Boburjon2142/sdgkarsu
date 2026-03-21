from django.db.models import Q
from django.http import Http404
from rest_framework import generics, permissions

from apps.accounts.models import User
from apps.common.throttling import SensitiveActionRateThrottle

from .models import Project
from .permissions import CanAccessProject, CanManageProject
from .serializers import ProjectCreateSerializer, ProjectDocumentCreateSerializer
from .services import create_project, create_project_document, delete_project, update_project


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectCreateSerializer
    search_fields = ("title", "description")
    ordering_fields = ("created_at", "updated_at", "title")

    def get_queryset(self):
        user = self.request.user
        queryset = Project.objects.select_related("owner").prefetch_related("members", "documents")
        if user.role == User.Role.ADMIN:
            return queryset
        return queryset.filter(Q(owner=user) | Q(members=user)).distinct()

    def perform_create(self, serializer):
        if self.request.user.role not in {User.Role.ADMIN, User.Role.MANAGER}:
            self.permission_denied(self.request, message="You do not have permission to create projects.")
        create_project(self.request, serializer)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.select_related("owner").prefetch_related("members", "documents")
    serializer_class = ProjectCreateSerializer
    throttle_classes = [SensitiveActionRateThrottle]

    def get_object(self):
        obj = super().get_object()
        if self.request.method in permissions.SAFE_METHODS:
            if not CanAccessProject().has_object_permission(self.request, self, obj):
                raise Http404
            return obj
        if not CanManageProject().has_object_permission(self.request, self, obj):
            self.permission_denied(self.request, message="You do not have permission to modify this project.")
        return obj

    def perform_update(self, serializer):
        update_project(self.request, serializer)

    def perform_destroy(self, instance):
        delete_project(self.request, instance)


class ProjectDocumentCreateView(generics.CreateAPIView):
    serializer_class = ProjectDocumentCreateSerializer
    throttle_classes = [SensitiveActionRateThrottle]

    def get_project(self):
        project = generics.get_object_or_404(Project, pk=self.kwargs["project_id"])
        if not CanManageProject().has_object_permission(self.request, self, project):
            self.permission_denied(self.request, message="You do not have permission to upload documents to this project.")
        return project

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project"] = self.get_project()
        return context

    def perform_create(self, serializer):
        create_project_document(self.request, serializer)
