from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterUserTest(APITestCase):

    def test_registration(self):
        data = {
            "password": "123456usa",
            "password2": "123456usa",
            "email": "usamamashood2@gmail.com",
            "first_name": "usama",
            "last_name": "mashood"
        }
        response = self.client.post('/accounts/register', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_token(self):
        user = User.objects.create_user(username='admin',
                                        password='some-very-strong-psw'
                                        )
        data = {
            'username': 'admin',
            'password': 'some-very-strong-psw'

        }
        response = self.client.post('/accounts/token', data)

        self.refresh = response.data['refresh']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
