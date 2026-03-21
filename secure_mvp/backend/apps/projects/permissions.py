from rest_framework.permissions import BasePermission

from apps.accounts.models import User


class CanAccessProject(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == User.Role.ADMIN:
            return True
        return obj.owner_id == request.user.id or obj.members.filter(id=request.user.id).exists()


class CanManageProject(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == User.Role.ADMIN:
            return True
        if request.user.role != User.Role.MANAGER:
            return False
        return obj.owner_id == request.user.id
