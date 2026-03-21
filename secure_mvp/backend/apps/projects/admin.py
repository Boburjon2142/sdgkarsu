from django.contrib import admin

from .models import Project, ProjectDocument


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "description", "owner__email")
    filter_horizontal = ("members",)


@admin.register(ProjectDocument)
class ProjectDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "uploaded_by", "created_at")
    search_fields = ("title", "project__title", "uploaded_by__email")
