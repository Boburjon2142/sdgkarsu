from django.contrib.auth import get_user_model
from django.test import override_settings
from django.test import TestCase
from rest_framework.test import APIClient

from apps.projects.models import Project


User = get_user_model()


class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=False)
        self.admin_user = User.objects.create_user(
            email="admin@example.com",
            username="admin",
            role="admin",
            password="StrongPassword123!",
        )
        self.manager_user = User.objects.create_user(
            email="manager@example.com",
            username="manager",
            role="manager",
            password="StrongPassword123!",
        )
        self.member_user = User.objects.create_user(
            email="member-existing@example.com",
            username="memberexisting",
            role="member",
            password="StrongPassword123!",
        )

    def test_register_logs_user_in(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "email": "member@example.com",
                "username": "member1",
                "first_name": "A",
                "last_name": "B",
                "password": "StrongPassword123!",
                "password_confirm": "StrongPassword123!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["email"], "member@example.com")

    def test_non_member_cannot_read_other_private_project(self):
        owner = User.objects.create_user(email="owner@example.com", username="owner", password="StrongPassword123!")
        stranger = User.objects.create_user(email="stranger@example.com", username="stranger", password="StrongPassword123!")
        project = Project.objects.create(owner=owner, title="Secret", description="Test project body")

        self.client.force_authenticate(user=stranger)
        response = self.client.get(f"/api/projects/{project.id}/")
        self.assertEqual(response.status_code, 404)

    @override_settings(ADMIN_URL="internal-admin/")
    def test_admin_url_is_not_default(self):
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 404)

    def test_admin_can_list_users(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get("/api/auth/users/")
        self.assertEqual(response.status_code, 200)

    def test_non_admin_cannot_list_users(self):
        self.client.force_authenticate(user=self.manager_user)
        response = self.client.get("/api/auth/users/")
        self.assertEqual(response.status_code, 403)

    def test_unauthenticated_user_cannot_access_me(self):
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.status_code, 403)
