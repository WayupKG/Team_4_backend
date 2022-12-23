from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.urls.base import reverse

from ..serializers import UserSerializer

User = get_user_model()


class UserAPITestCase(APITestCase):
    """Тестирование Пользователя"""
    def setUp(self) -> None:
        self.user_1 = User.objects.create(email='test@mail.ru', first_name='Robert', last_name='Robertov',
                                          phone='09994284953', password='Fg355htddg3')

        self.user_2 = User.objects.create(email='test3@list.ru', first_name='Adilet', last_name='Alekseev',
                                          phone='0707366749', password='123456789AAa')

        self.user_3 = User.objects.create(email='test1@icloud.com', first_name='Kristian', last_name='Kambarov',
                                          phone='0834234234', password='24688Ader')

    def test_get_user(self):
        url = reverse('user-detail', kwargs={"pk": self.user_3.id})
        serializer = UserSerializer(self.user_3)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_update_user(self):
        url = reverse('user-detail', kwargs={"pk": self.user_2.id})
        new_user_data = {
            'email': self.user_2.email,
            'first_name': 'Acol',
            'last_name': 'Moldoakynove',
            'phone': self.user_2.phone
        }
        serializer = UserSerializer(new_user_data)
        response = self.client.put(url, data=new_user_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_delete_user(self):
        url = reverse('user-detail', kwargs={"pk": self.user_1.id})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_registration_user(self):
        url = reverse('user-registration')
        user_data = {
            "email": "roberTest@example.com",
            "first_name": "Vlad",
            "last_name": "Vladov",
            "phone": "996707323445",
            "password": "123456789",
            "password_confirm": "123456789"
        }
        success_return = 'Thanks for registration. Activate your account via link in your mail'
        response = self.client.post(url, data=user_data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(success_return, response.data)
