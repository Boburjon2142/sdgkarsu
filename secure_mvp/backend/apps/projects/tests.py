from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Project


User = get_user_model()


class ProjectTests(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=False)
        self.manager = User.objects.create_user(
            email="manager@example.com",
            username="manager",
            role="manager",
            password="StrongPassword123!",
        )
        self.member = User.objects.create_user(
            email="member@example.com",
            username="member",
            role="member",
            password="StrongPassword123!",
        )
        self.admin_user = User.objects.create_user(
            email="admin@example.com",
            username="admin",
            role="admin",
            password="StrongPassword123!",
        )

    def test_manager_can_create_project(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.post(
            "/api/projects/",
            {
                "title": "Security Rollout",
                "description": "Deliver secure production controls.",
                "status": "active",
                "member_ids": [self.member.id],
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Project.objects.count(), 1)

    def test_invalid_document_extension_is_rejected(self):
        project = Project.objects.create(owner=self.manager, title="Project One", description="Long enough description")
        self.client.force_authenticate(user=self.manager)
        bad_file = SimpleUploadedFile("shell.exe", b"binary", content_type="application/octet-stream")
        response = self.client.post(
            f"/api/projects/{project.id}/documents/",
            {"title": "Bad", "file": bad_file},
        )
        self.assertEqual(response.status_code, 400)

    def test_admin_user_cannot_be_added_as_project_member(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.post(
            "/api/projects/",
            {
                "title": "Restricted Members",
                "description": "Trying to add an admin as a member.",
                "status": "active",
                "member_ids": [self.admin_user.id],
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_member_cannot_create_project(self):
        self.client.force_authenticate(user=self.member)
        response = self.client.post(
            "/api/projects/",
            {
                "title": "Member Create Attempt",
                "description": "Members should not be allowed to create projects.",
                "status": "active",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_unauthenticated_user_cannot_list_projects(self):
        response = self.client.get("/api/projects/")
        self.assertEqual(response.status_code, 403)
