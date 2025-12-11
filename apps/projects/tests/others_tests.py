from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from apps.projects.models import Project, ProjectState, ProjectType, ProjectPriority, ProjectLeader
from apps.users.models import User, Role
from apps.company.models import Company

class CompanyViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_role = Role.objects.create(name="admin")
        self.user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass',
            role=self.admin_role
        )
        self.client.force_authenticate(user=self.user)

    def test_list(self):
        Company.objects.create(name="Empresa Test", ruc="12345678901", address="Av. Siempre Viva 123")
        url = reverse("company-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create(self):
        url = reverse("company-list")
        data = {
            "name": "Empresa Nueva",
            "ruc": "98765432109",
            "address": "Calle Falsa 456"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "Empresa Nueva")

    def test_update(self):
        instance = Company.objects.create(name="Empresa Vieja", ruc="11111111111", address="Av. Los Antiguos 789")
        url = reverse("company-detail", args=[instance.id])
        response = self.client.patch(url, {"name": "Empresa Actualizada"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Empresa Actualizada")

    def test_delete(self):
        instance = Company.objects.create(name="Empresa Temporal", ruc="22222222222", address="Av. Borrable 999")
        url = reverse("company-detail", args=[instance.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Company.objects.filter(id=instance.id).exists())

    #  python .\manage.py test apps.projects.tests.others_tests
    # Found 4 test(s).
    # Creating test database for alias 'default'...
    # System check identified no issues (0 silenced).
    # ....
    # ----------------------------------------------------------------------
    # Ran 4 tests in 2.114s

    # OK
    # Destroying test database for alias 'default'...