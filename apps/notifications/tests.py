# apps/notifications/tests.py
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from apps.users.models import User, Role
from apps.company.models import Company
from apps.projects.models import Project
from apps.tasks.models import Task
from apps.notifications.models import Notification, NotificationType


class NotificationViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Crear usuario y autenticación
        self.admin_role = Role.objects.create(name="admin")
        self.user = User.objects.create_user(username="admin", email="admin@test.com", password="adminpass", role=self.admin_role)
        self.client.force_authenticate(user=self.user)

        # Crear tipos de notificación
        self.ntype = NotificationType.objects.create(code="info", name="Información")

        # Crear proyecto y tarea asociados a la notificación
        self.company = Company.objects.create(name="Empresa A", ruc="123456789")
        self.project = Project.objects.create(name="Proyecto X", company=self.company)
        self.task = Task.objects.create(title="Tarea 1", project=self.project)

        # Crear notificaciones para el usuario
        self.notification1 = Notification.objects.create(
            type=self.ntype,
            message="Mensaje 1",
            to_user=self.user,
            from_user=self.user,
            task=self.task
        )
        self.notification2 = Notification.objects.create(
            type=self.ntype,
            message="Mensaje 2",
            to_user=self.user,
            from_user=self.user,
            task=self.task
        )

    def test_list_user_notifications(self):
        url = reverse("notification-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data["results"]), 2)

    def test_recent_notifications(self):
        url = reverse("notification-recent-activity")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_all_notifications_paginated(self):
        url = reverse("notification-all-notifications")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
        self.assertLessEqual(len(response.data["results"]), 5)

    def test_delete_notification(self):
        url = reverse("notification-detail", args=[self.notification1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)


#  python manage.py test apps.notifications.tests
# Found 4 test(s).
# Creating test database for alias 'default'...
# System check identified no issues (0 silenced).
# ....
# ----------------------------------------------------------------------
# Ran 4 tests in 2.182s

# OK
# Destroying test database for alias 'default'...