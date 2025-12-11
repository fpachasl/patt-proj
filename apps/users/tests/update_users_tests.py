from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.users.models import Role

User = get_user_model()

class UpdateProfileTests(APITestCase):
    def setUp(self):
        self.user_role = Role.objects.create(name="colaborador")

        self.user = User.objects.create_user(
            username='testuser',
            email="test@example.com",
            password="strongpass",
            first_name="Test",
            last_name="User",
            cellphone="123456789",
            role=self.user_role
        )

    def test_update_profile_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("user-update-profile")
        payload = {
            "first_name": "Updated",
            "cellphone": "987654321"
        }

        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Updated")
        self.assertEqual(response.data["cellphone"], "987654321")

    def test_update_profile_unauthenticated(self):
        url = reverse("user-update-profile")
        payload = {
            "first_name": "Malicious"
        }

        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    #  python .\manage.py test apps.users.tests.update_users_tests
    # Found 2 test(s).
    # Creating test database for alias 'default'...
    # System check identified no issues (0 silenced).
    # ..
    # ----------------------------------------------------------------------
    # Ran 2 tests in 1.140s

    # OK
    # Destroying test database for alias 'default'...