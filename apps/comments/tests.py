from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.users.models import User, Role
from apps.projects.models import Project, ProjectState, ProjectType, ProjectPriority
from apps.tasks.models import Task, TaskState, ProjectArea
from apps.comments.models import Comment, CommentAttachment
from apps.company.models import Company
from datetime import date

class CommentViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Roles y usuarios
        self.admin_role = Role.objects.create(name="admin")
        self.user = User.objects.create_user(username="admin", email="admin@test.com", password="adminpass", role=self.admin_role)
        self.client.force_authenticate(user=self.user)

        # Proyecto y tarea
        self.company = Company.objects.create(name="Empresa X", ruc="12345678901")
        self.state = ProjectState.objects.create(code="active", name="Activo")
        self.ptype = ProjectType.objects.create(code="software", name="Software")
        self.priority = ProjectPriority.objects.create(code="high", name="Alta")

        self.project = Project.objects.create(
            name="Proyecto Comentario",
            project_state=self.state,
            project_type=self.ptype,
            priority=self.priority,
            company=self.company
        )
        self.area = ProjectArea.objects.create(project=self.project, name="Área 1")

        self.task_state = TaskState.objects.create(code="planning", name="Planificada")
        self.task = Task.objects.create(
            title="Tarea Comentario",
            description="Tarea para pruebas",
            project=self.project,
            area=self.area,
            task_state=self.task_state,
            start_date=date.today()
        )

    def test_create_comment_without_attachment(self):
        url = reverse("comment-list")
        data = {
            "content": "Este es un comentario de prueba",
            "task": self.task.id,
            "is_internal": True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)

    def test_create_comment_with_attachment(self):
        url = reverse("comment-list")
        file = SimpleUploadedFile("archivo.txt", b"Contenido del archivo")
        data = {
            "content": "Comentario con archivo",
            "task": self.task.id,
            "is_internal": False,
            "attachments": [file],
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(CommentAttachment.objects.count(), 1)

    def test_list_comments(self):
        Comment.objects.create(content="Comentario A", task=self.task, comment_user=self.user)
        Comment.objects.create(content="Comentario B", task=self.task, comment_user=self.user)

        url = reverse("comment-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 2)

    def test_list_comments_by_task(self):
        other_task = Task.objects.create(
            title="Otra tarea",
            description="desc",
            project=self.project,
            area=self.area,
            task_state=self.task_state,
        )
        Comment.objects.create(content="Comentario 1", task=self.task, comment_user=self.user)
        Comment.objects.create(content="Comentario 2", task=other_task, comment_user=self.user)

        url = reverse("comment-list") + f"?task={self.task.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(str(response.data[0]["task"]), str(self.task.id))

    #  python .\manage.py test apps.comments.tests
    # Found 4 test(s).
    # Creating test database for alias 'default'...
    # System check identified no issues (0 silenced).
    # ....
    # ----------------------------------------------------------------------
    # Ran 4 tests in 2.343s

    # OK
    # Destroying test database for alias 'default'...