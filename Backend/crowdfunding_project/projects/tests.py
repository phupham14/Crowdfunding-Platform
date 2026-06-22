from decimal import Decimal
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from interactions.models import UserInteraction
from projects.models import Project

User = get_user_model()


class ProjectBrowsingTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@example.com",
            password="123456",
            full_name="Project Owner",
            role="PROJECT_OWNER",
        )
        self.investor = User.objects.create_user(
            email="investor@example.com",
            password="123456",
            full_name="Investor",
            role="INVESTOR",
        )
        self.admin = User.objects.create_user(
            email="admin@example.com",
            password="123456",
            full_name="Admin",
            role="ADMIN",
        )
        self.open_project = Project.objects.create(
            owner=self.owner,
            name="Solar Farm",
            category="Energy",
            location="Da Nang",
            funding_target=Decimal("1000000.00"),
            status="OPEN",
        )
        self.pending_project = Project.objects.create(
            owner=self.owner,
            name="Pending Factory",
            category="Business",
            funding_target=Decimal("500000.00"),
            status="PENDING",
        )

    def test_public_project_list_only_returns_open_projects(self):
        response = self.client.get("/api/projects/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project_ids = {item["id"] for item in response.data}
        self.assertIn(self.open_project.id, project_ids)
        self.assertNotIn(self.pending_project.id, project_ids)

    def test_authenticated_retrieve_records_view_and_click_interactions(self):
        self.client.force_authenticate(user=self.investor)

        response = self.client.get(f"/api/projects/{self.open_project.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            UserInteraction.objects.filter(
                user=self.investor,
                project=self.open_project,
                interaction_type="view",
            ).count(),
            1,
        )
        self.assertEqual(
            UserInteraction.objects.filter(
                user=self.investor,
                project=self.open_project,
                interaction_type="click",
            ).count(),
            1,
        )

    def test_investor_cannot_create_project(self):
        self.client.force_authenticate(user=self.investor)

        response = self.client.post("/api/projects/", self._project_payload(), format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_project_owner_cannot_override_managed_fields_on_create(self):
        self.client.force_authenticate(user=self.owner)
        payload = {
            **self._project_payload(),
            "status": "OPEN",
            "raised": "999999.00",
            "is_disbursed": True,
            "total_repaid": "1000.00",
            "risk_level": 5,
        }

        response = self.client.post("/api/projects/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        project = Project.objects.get(id=response.data["id"])
        self.assertEqual(project.status, "PENDING")
        self.assertEqual(project.raised, Decimal("0.00"))
        self.assertFalse(project.is_disbursed)
        self.assertEqual(project.total_repaid, Decimal("0.00"))

    def test_only_admin_can_change_project_status(self):
        url = f"/api/projects/{self.open_project.id}/change-status/"

        self.client.force_authenticate(user=self.owner)
        owner_response = self.client.post(url, {"status": "CANCELLED"}, format="json")
        self.assertEqual(owner_response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin)
        admin_response = self.client.post(url, {"status": "CANCELLED"}, format="json")
        self.assertEqual(admin_response.status_code, status.HTTP_200_OK)

        self.open_project.refresh_from_db()
        self.assertEqual(self.open_project.status, "CANCELLED")

    def _project_payload(self):
        now = timezone.now()
        return {
            "name": "Wind Farm",
            "category": "Energy",
            "description": "Renewable energy project",
            "location": "Hue",
            "funding_target": "750000.00",
            "apr_expected": "0.12",
            "start_at": now.isoformat(),
            "end_at": (now + timedelta(days=120)).isoformat(),
            "min_invest_amount": "1000.00",
            "max_invest_amount": "100000.00",
            "min_invest_duration_months": 6,
        }
