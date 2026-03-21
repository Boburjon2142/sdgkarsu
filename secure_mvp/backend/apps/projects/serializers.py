from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Project, ProjectDocument


User = get_user_model()


class ProjectDocumentSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProjectDocument
        fields = ("id", "title", "file", "uploaded_by", "created_at")
        read_only_fields = ("id", "uploaded_by", "created_at")


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(
        source="members",
        queryset=User.objects.filter(is_active=True),
        many=True,
        required=False,
        write_only=True,
    )
    documents = ProjectDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ("id", "title", "description", "status", "owner", "member_ids", "documents", "created_at", "updated_at")
        read_only_fields = ("id", "owner", "documents", "created_at", "updated_at")

    def validate_title(self, value):
        cleaned = value.strip()
        if len(cleaned) < 4:
            raise serializers.ValidationError("Title must be at least 4 characters long.")
        return cleaned

    def validate_description(self, value):
        cleaned = value.strip()
        if len(cleaned) < 10:
            raise serializers.ValidationError("Description must be at least 10 characters long.")
        return cleaned

    def validate_member_ids(self, members):
        seen_ids = set()
        cleaned_members = []
        for member in members:
            if member.id in seen_ids:
                continue
            seen_ids.add(member.id)
            if member.role == "admin" or member.is_superuser:
                raise serializers.ValidationError("Admin users cannot be assigned as project members.")
            cleaned_members.append(member)
        return cleaned_members


class ProjectCreateSerializer(ProjectSerializer):
    def create(self, validated_data):
        members = validated_data.pop("members", [])
        request = self.context["request"]
        project = Project.objects.create(owner=request.user, **validated_data)
        if members:
            project.members.set(members)
        return project

    def update(self, instance, validated_data):
        members = validated_data.pop("members", None)
        for field in ("title", "description", "status"):
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()
        if members is not None:
            instance.members.set(members)
        return instance


class ProjectDocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDocument
        fields = ("id", "title", "file", "created_at")
        read_only_fields = ("id", "created_at")

    def create(self, validated_data):
        return ProjectDocument.objects.create(
            uploaded_by=self.context["request"].user,
            project=self.context["project"],
            **validated_data,
        )
