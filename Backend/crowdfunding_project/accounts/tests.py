from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models.project_owner_application import ProjectOwnerApplication
from accounts.models.wallet import Wallet

User = get_user_model()


class AuthenticationTests(APITestCase):
    def test_register_creates_investor_account_and_wallet(self):
        response = self.client.post(
            reverse("user-register"),
            {
                "email": "investor@example.com",
                "full_name": "Investor User",
                "phone": "0900000001",
                "password": "StrongPass123",
                "role": "ADMIN",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email="investor@example.com")
        self.assertEqual(user.role, "INVESTOR")
        self.assertTrue(user.check_password("StrongPass123"))
        self.assertTrue(Wallet.objects.filter(user=user).exists())

    def test_login_returns_jwt_tokens_and_role(self):
        User.objects.create_user(
            email="investor@example.com",
            password="StrongPass123",
            full_name="Investor User",
            role="INVESTOR",
        )

        response = self.client.post(
            reverse("user-login"),
            {"email": "investor@example.com", "password": "StrongPass123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["role"], "INVESTOR")

    def test_login_rejects_invalid_password(self):
        User.objects.create_user(
            email="investor@example.com",
            password="StrongPass123",
            full_name="Investor User",
            role="INVESTOR",
        )

        response = self.client.post(
            reverse("user-login"),
            {"email": "investor@example.com", "password": "wrong-password"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProjectOwnerApplicationTests(APITestCase):
    def setUp(self):
        self.investor = User.objects.create_user(
            email="applicant@example.com",
            password="123456",
            full_name="Applicant",
            role="INVESTOR",
        )
        self.project_owner = User.objects.create_user(
            email="owner-role@example.com",
            password="123456",
            full_name="Existing Owner",
            role="PROJECT_OWNER",
        )
        self.admin = User.objects.create_user(
            email="admin@example.com",
            password="123456",
            full_name="Admin",
            role="ADMIN",
        )

    def test_get_my_application_returns_404_when_not_submitted(self):
        self.client.force_authenticate(user=self.investor)

        response = self.client.get("/api/accounts/project-owner-applications/me/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_investor_can_submit_project_owner_application(self):
        self.client.force_authenticate(user=self.investor)

        response = self.client.post(
            "/api/accounts/project-owner-applications/me/",
            {
                "business_name": "Green Farm Co",
                "business_type": "Agriculture",
                "tax_code": "TAX-001",
                "bio": "Sustainable farming business",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "PENDING")
        self.assertTrue(
            ProjectOwnerApplication.objects.filter(
                user=self.investor,
                business_name="Green Farm Co",
                status="PENDING",
            ).exists()
        )

    def test_project_owner_cannot_submit_application(self):
        self.client.force_authenticate(user=self.project_owner)

        response = self.client.post(
            "/api/accounts/project-owner-applications/me/",
            {"business_name": "Already Owner Co"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "Only investors can submit project owner applications",
        )

    def test_admin_can_list_project_owner_applications(self):
        ProjectOwnerApplication.objects.create(
            user=self.investor,
            business_name="Green Farm Co",
        )
        self.client.force_authenticate(user=self.admin)

        response = self.client.get("/api/accounts/project-owner-applications/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user_email"], self.investor.email)

    def test_admin_approve_application_changes_user_role(self):
        application = ProjectOwnerApplication.objects.create(
            user=self.investor,
            business_name="Green Farm Co",
        )
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            f"/api/accounts/project-owner-applications/{application.id}/approve/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "APPROVED")

        self.investor.refresh_from_db()
        application.refresh_from_db()
        self.assertEqual(self.investor.role, "PROJECT_OWNER")
        self.assertEqual(application.reviewed_by, self.admin)
        self.assertIsNotNone(application.reviewed_at)

    def test_reject_application_requires_reason(self):
        application = ProjectOwnerApplication.objects.create(
            user=self.investor,
            business_name="Green Farm Co",
        )
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            f"/api/accounts/project-owner-applications/{application.id}/reject/",
            {"reject_reason": ""},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("reject_reason", response.data)
