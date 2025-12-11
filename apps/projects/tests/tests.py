from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from apps.projects.models import Project, ProjectState, ProjectType, ProjectPriority, ProjectLeader
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

        ProjectLeader.objects.create(project=self.project, leader=self.leader)

    def test_assigned_projects_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("project-assigned-projects")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data), 1)

    def test_assigned_projects_leader(self):
        self.client.force_authenticate(user=self.leader)
        url = reverse("project-assigned-projects")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["id"], str(self.project.id))

    def test_assigned_projects_unauthenticated(self):
        url = reverse("project-assigned-projects")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 401)

    
    #  python .\manage.py test apps.projects.tests.tests
    # Found 3 test(s).
    # Creating test database for alias 'default'...
    # System check identified no issues (0 silenced).
    # ...
    # ----------------------------------------------------------------------
    # Ran 3 tests in 5.358s

    # OK
    # Destroying test database for alias 'default'...