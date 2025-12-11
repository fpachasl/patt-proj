from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.users.models import User, Role
from apps.company.models import Company
from apps.projects.models import Project, ProjectArea, ProjectLeader
from apps.tasks.models import Task
from apps.documents.models import Document, DocumentType


class DocumentViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Roles y usuarios
        self.admin_role = Role.objects.create(name="admin")
        self.user = User.objects.create_user(
            username="admin", email="admin@test.com", password="adminpass", role=self.admin_role
        )
        self.client.force_authenticate(user=self.user)

        # Relacionados
        self.company = Company.objects.create(name="Empresa A", ruc="11111111111")
        self.project = Project.objects.create(name="Proyecto X", company=self.company)
        self.area = ProjectArea.objects.create(name="Área 1", project=self.project)
        self.task = Task.objects.create(title="Tarea A", project=self.project, area=self.area)

        # Asignar como líder del proyecto
        ProjectLeader.objects.create(project=self.project, leader=self.user)

        # Tipo de documento
        self.doc_type = DocumentType.objects.create(code="pdf", name="PDF")

        # Documento
        self.document = Document.objects.create(
            name="Doc Prueba",
            project=self.project,
            area=self.area,
            task=self.task,
            document_type=self.doc_type,
            uploaded_by=self.user,
        )

    def test_list_documents(self):
        url = reverse("document-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_create_document(self):
        url = reverse("document-list")
        file = SimpleUploadedFile("testfile.pdf", b"contenido de prueba", content_type="application/pdf")
        data = {
            "name": "Documento Test",
            "file": file,
            "project_id": str(self.project.id),
            "area": str(self.area.id),
            "task": str(self.task.id),
            "document_type_id": str(self.doc_type.id),
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, 201)

    def test_delete_document(self):
        url = reverse("document-detail", args=[self.document.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)


class DocumentTypeViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_role = Role.objects.create(name="admin")
        self.user = User.objects.create_user(username="admin", email="admin@test.com", password="adminpass", role=self.admin_role)
        self.client.force_authenticate(user=self.user)
        self.type = DocumentType.objects.create(code="docx", name="Word")

    def test_list_types(self):
        url = reverse("documenttype-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_type(self):
        url = reverse("documenttype-list")
        res = self.client.post(url, {"code": "xls", "name": "Excel"})
        self.assertEqual(res.status_code, 201)

    def test_update_type(self):
        url = reverse("documenttype-detail", args=[self.type.id])
        res = self.client.patch(url, {"name": "MS Word"})
        self.assertEqual(res.status_code, 200)

    def test_delete_type(self):
        url = reverse("documenttype-detail", args=[self.type.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, 204)


#  python .\manage.py test apps.documents.tests
# Found 7 test(s).
# Creating test database for alias 'default'...
# System check identified no issues (0 silenced).
# .......
# ----------------------------------------------------------------------
# Ran 7 tests in 4.078s

# OK
# Destroying test database for alias 'default'...