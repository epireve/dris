from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import DisasterReport, AidRequest, User


class AidRequestTests(TestCase):
    def setUp(self):
        # Create test users with different roles
        self.citizen = get_user_model().objects.create_user(
            username="testcitizen",
            password="testpass123",
            email="citizen@test.com",
            role="CITIZEN",
        )
        self.volunteer = get_user_model().objects.create_user(
            username="testvolunteer",
            password="testpass123",
            email="volunteer@test.com",
            role="VOLUNTEER",
        )
        self.authority = get_user_model().objects.create_user(
            username="testauthority",
            password="testpass123",
            email="authority@test.com",
            role="AUTHORITY",
        )

        # Create a test disaster report
        self.disaster_report = DisasterReport.objects.create(
            reporter=self.citizen,
            disaster_type="FLOOD",
            description="Test flood in area",
            latitude=3.140853,
            longitude=101.693207,
            severity="HIGH",
        )

        # Create a test aid request
        self.aid_request = AidRequest.objects.create(
            requester=self.citizen,
            disaster_report=self.disaster_report,
            aid_type="FOOD",
            description="Need emergency food supplies",
            quantity=50,
            priority="HIGH",
            location_details="123 Test Street",
        )

        self.client = Client()

    def test_aid_request_creation(self):
        """Test creating a new aid request"""
        self.client.login(username="testcitizen", password="testpass123")

        data = {
            "aid_type": "WATER",
            "description": "Need clean water supplies",
            "quantity": 100,
            "priority": "URGENT",
            "location_details": "456 Test Avenue",
            "disaster_report": self.disaster_report.id,
        }

        response = self.client.post(reverse("submit_aid_request"), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success

        # Verify aid request was created
        aid_request = AidRequest.objects.get(requester=self.citizen, aid_type="WATER")
        self.assertEqual(aid_request.description, "Need clean water supplies")
        self.assertEqual(aid_request.quantity, 100)
        self.assertEqual(aid_request.status, "PENDING")

    def test_aid_request_listing(self):
        """Test aid request listing for different user roles"""
        # Test citizen view (should only see own requests)
        self.client.login(username="testcitizen", password="testpass123")
        response = self.client.get(reverse("aid_request_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["requests"]), 1)

        # Test volunteer view (should see pending and in-progress requests)
        self.client.login(username="testvolunteer", password="testpass123")
        response = self.client.get(reverse("aid_request_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["requests"]), 1)

        # Test authority view (should see all requests)
        self.client.login(username="testauthority", password="testpass123")
        response = self.client.get(reverse("aid_request_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["requests"]), 1)

    def test_aid_request_status_update(self):
        """Test updating aid request status by volunteer/authority"""
        self.client.login(username="testvolunteer", password="testpass123")

        data = {"status": "IN_PROGRESS", "notes": "Processing this request"}

        response = self.client.post(
            reverse("aid_request_detail", kwargs={"pk": self.aid_request.pk}), data
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success

        # Verify status was updated
        aid_request = AidRequest.objects.get(pk=self.aid_request.pk)
        self.assertEqual(aid_request.status, "IN_PROGRESS")
        self.assertEqual(aid_request.assigned_to, self.volunteer)
        self.assertIn("Processing this request", aid_request.notes)

    def test_disaster_report_aid_request_link(self):
        """Test linking aid requests to disaster reports"""
        self.client.login(username="testcitizen", password="testpass123")

        # Get disaster report detail page
        response = self.client.get(
            reverse("disaster_report_detail", kwargs={"pk": self.disaster_report.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Associated Aid Requests")
        self.assertContains(response, "Need emergency food supplies")

        # Test submitting new aid request with disaster report link
        response = self.client.post(
            reverse("submit_aid_request"),
            {
                "aid_type": "SHELTER",
                "description": "Need temporary shelter",
                "priority": "HIGH",
                "location_details": "789 Emergency Road",
                "disaster_report": self.disaster_report.id,
            },
        )
        self.assertEqual(response.status_code, 302)

        # Verify the link in disaster report detail
        response = self.client.get(
            reverse("disaster_report_detail", kwargs={"pk": self.disaster_report.pk})
        )
        self.assertContains(response, "Need temporary shelter")
