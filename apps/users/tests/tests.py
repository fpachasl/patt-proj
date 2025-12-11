from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()

class UserViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email="testuser@example.com",
            password="strongpassword123",
            first_name="Test",
            last_name="User",
            cellphone="965131706"
        )
    # Verifica que un usuario autenticado pueda obtener correctamente su perfil
    def test_get_profile_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("user-get-profile")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertEqual(response.data["id"], str(self.user.id))
    # Verifica que un usuario no autenticado no pueda acceder al perfil.
    def test_get_profile_unauthenticated(self):
        url = reverse("user-get-profile")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    #  python .\manage.py test apps.users.tests
    # Found 2 test(s).
    # Creating test database for alias 'default'...
    # System check identified no issues (0 silenced).
    # ..
    # ----------------------------------------------------------------------
    # Ran 2 tests in 1.045s

    # OK
    # Destroying test database for alias 'default'...