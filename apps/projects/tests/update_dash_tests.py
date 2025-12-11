from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from apps.projects.models import (
    Project, ProjectState, ProjectType, ProjectPriority, ProjectLeader,
    ProjectArea, ProjectAreaMember
)
from apps.users.models import User, Role
from apps.company.models import Company

class ProjectViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Crear roles
        self.admin_role = Role.objects.create(id=1, name="admin")
        self.leader_role = Role.objects.create(id=2, name="líder")
        self.member_role = Role.objects.create(id=3, name="miembro")

        # Usuarios
        self.admin = User.objects.create_user(username='admin', email='admin@test.com', password='adminpass', role=self.admin_role)
        self.leader = User.objects.create_user(username='leader', email='leader@test.com', password='leaderpass', role=self.leader_role)
        self.member = User.objects.create_user(username='member', email='member@test.com', password='memberpass', role=self.member_role)

        # Proyecto base
        self.state = ProjectState.objects.create(code="planning", name="Planeado")
        self.ptype = ProjectType.objects.create(code="internal", name="Interno")
        self.priority = ProjectPriority.objects.create(code="high", name="Alta")
        self.company = Company.objects.create(name="Empresa X", ruc="12345678901")

        self.project = Project.objects.create(
            name="Proyecto Test",
            project_state=self.state,
            project_type=self.ptype,
            priority=self.priority,
            company=self.company
        )

        # Asignar líder
        ProjectLeader.objects.create(project=self.project, leader=self.leader)

    def test_dashboard_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("project-get-dashboard")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIn("total", res.data)
        self.assertIn("planning", res.data)

    def test_dashboard_leader(self):
        self.client.force_authenticate(user=self.leader)
        url = reverse("project-get-dashboard")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIn("total", res.data)
        self.assertEqual(res.data["total"], 1)

    def test_dashboard_member(self):
        area = ProjectArea.objects.create(project=self.project, name="Área A")
        ProjectAreaMember.objects.create(area=area, user=self.member)
        self.client.force_authenticate(user=self.member)
        url = reverse("project-get-dashboard")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIn("projects_assigned", res.data)
        self.assertIn("pending_tasks", res.data)

    def test_update_project_by_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("project-update-project")
        data = {
            "project_id": str(self.project.id),
            "name": "Nuevo nombre del proyecto",
            "description": "Descripción actualizada"
        }
        res = self.client.put(url, data, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["data"]["name"], "Nuevo nombre del proyecto")

    def test_update_project_forbidden_for_member(self):
        self.client.force_authenticate(user=self.member)
        url = reverse("project-update-project")
        data = {
            "project_id": str(self.project.id),
            "name": "Nombre no autorizado"
        }
        res = self.client.put(url, data, format='json')
        self.assertEqual(res.status_code, 403)

    def test_update_project_missing_id(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("project-update-project")
        res = self.client.put(url, {}, format='json')
        self.assertEqual(res.status_code, 400)

    #  python .\manage.py test apps.projects.tests.update_dash_tests
    # Found 6 test(s).
    # Creating test database for alias 'default'...
    # System check identified no issues (0 silenced).
    # ......
    # ----------------------------------------------------------------------
    # Ran 6 tests in 11.502s

    # OK
    # Destroying test database for alias 'default'...