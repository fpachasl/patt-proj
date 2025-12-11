from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from apps.projects.models import Project, ProjectArea, ProjectLeader, ProjectState, ProjectType, ProjectPriority
from apps.tasks.models import Task, TaskState
from apps.users.models import User, Role
from apps.company.models import Company
from datetime import date

class TaskViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Roles y usuarios
        self.admin_role = Role.objects.create(name="admin")
        self.leader_role = Role.objects.create(name="líder")
        self.member_role = Role.objects.create(name="miembro")

        self.admin = User.objects.create_user(username="admin", email="admin@test.com", password="adminpass", role=self.admin_role)
        self.leader = User.objects.create_user(username="leader", email="leader@test.com", password="leaderpass", role=self.leader_role)
        self.member = User.objects.create_user(username="member", email="member@test.com", password="memberpass", role=self.member_role)

        self.client.force_authenticate(user=self.admin)

        # Datos base
        self.state = ProjectState.objects.create(code="active", name="Activo")
        self.ptype = ProjectType.objects.create(code="software", name="Software")
        self.priority = ProjectPriority.objects.create(code="high", name="Alta")
        self.company = Company.objects.create(name="Empresa X", ruc="12345678901")

        self.project = Project.objects.create(
            name="Proyecto A",
            project_state=self.state,
            project_type=self.ptype,
            priority=self.priority,
            company=self.company
        )

        self.area = ProjectArea.objects.create(project=self.project, name="Backend", description="Área de backend")
        ProjectLeader.objects.create(project=self.project, leader=self.leader)

        self.task_state = TaskState.objects.create(code="planning", name="Planificada")
        self.task = Task.objects.create(
            title="Tarea de prueba",
            description="Descripción",
            task_state=self.task_state,
            project=self.project,
            area=self.area,
            assigned_user=self.member,
            assigned_by=self.leader,
            start_date=date.today()
        )

    def test_list_tasks(self):
        url = reverse("task-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        url = reverse("task-list")
        data = {
            "title": "Tarea nueva",
            "description": "Detalle",
            "task_state": self.task_state.id,
            "project": self.project.id,
            "area": self.area.id,
            "assigned_user": self.member.id,
            "assigned_by": self.admin.id,
            "start_date": date.today(),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_assigned_tasks(self):
        self.client.force_authenticate(user=self.member)
        url = reverse("task-assigned")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_task_detail_allowed(self):
        self.client.force_authenticate(user=self.member)
        url = reverse("task-task-detail", args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(self.task.id))

    def test_task_detail_unauthorized(self):
        another_user = User.objects.create_user(username="otro", email="otro@test.com", password="test", role=self.member_role)
        self.client.force_authenticate(user=another_user)
        url = reverse("task-task-detail", args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_update_state_authorized(self):
        self.client.force_authenticate(user=self.member)
        new_state = TaskState.objects.create(code="done", name="Hecho")
        url = reverse("task-update-state", args=[self.task.id])
        response = self.client.patch(url, {"task_state": new_state.id})
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.task_state.id, new_state.id)

    def test_by_project_as_leader(self):
        self.client.force_authenticate(user=self.leader)
        url = reverse("task-by-project", kwargs={"project_id": self.project.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_assign_user_admin(self):
        url = reverse("task-assign-user")
        data = {
            "task_id": self.task.id,
            "assigned_user": self.admin.id
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.assigned_user.id, self.admin.id)

    #  python .\manage.py test apps.tasks.tests.tests
    # Found 8 test(s).
    # Creating test database for alias 'default'...
    # System check identified no issues (0 silenced).
    # ........
    # ----------------------------------------------------------------------
    # Ran 8 tests in 16.068s

    # OK
    # Destroying test database for alias 'default'...