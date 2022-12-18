from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model
from django.urls.base import reverse

User = get_user_model()


class AuthAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user_data = dict(email='aba@mail.ru', first_name='Robert', last_name='Robertov',
                              phone='0995404343', password='123456789')
        self.user = User.objects.create_user(**self.user_data)

    def test_login(self):
        url_login = reverse('login')
        url_logout = reverse('logout')
        response = self.client.post(url_login, data=self.user_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn('auth_token', response.data)
