from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apps.users.models import Role

User = get_user_model()

class UserViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin_role = Role.objects.create(name="admin")
        self.user_role = Role.objects.create(name="colaborador")

        # Usuario regular
        self.user = User.objects.create_user(
            username='testuser',
            email="testuser@example.com",
            password="strongpassword123",
            first_name="Test",
            last_name="User",
            cellphone="965131706",
            role=self.user_role,
        )

        # Usuario admin
        self.admin, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                "email": "admin@example.com",
                "first_name": "Admin",
                "last_name": "User",
                "cellphone": "999999999",
                "role": self.admin_role,
            }
        )
        self.admin.set_password("adminpass")
        self.admin.save()

    def test_get_user_by_id_as_self(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("user-get-user-by-id", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(self.user.id))

    def test_get_user_by_id_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("user-get-user-by-id", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_user_by_id_unauthorized(self):
        other_user = User.objects.create_user(
            username='otheruser',
            email="other@example.com",
            password="pass",
            first_name="Other",
            last_name="User",
            cellphone="888888888",
            role=self.user_role  
        )
        self.client.force_authenticate(user=other_user)
        url = reverse("user-get-user-by-id", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    #  python .\manage.py test apps.users.tests.users_by_id_tests
    # Found 3 test(s).
    # Creating test database for alias 'default'...
    # System check identified no issues (0 silenced).
    # ...
    # ----------------------------------------------------------------------
    # Ran 3 tests in 4.186s

    # OK
    # Destroying test database for alias 'default'...