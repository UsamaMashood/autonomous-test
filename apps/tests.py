from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import App, Plan, Subscription

User = get_user_model()


class AppTest(APITestCase):

    app_list_url = reverse('app_list')

    def setUp(self):
        self.user = User.objects.create_user(username='admin',
                                        password='some-very-strong-psw'
                                        )

        data = {
            'username': 'admin',
            'password': 'some-very-strong-psw'

        }

        self.plan = Plan(price=0, name='free')
        self.plan.save()
        self.subscription = Subscription(plan=self.plan, active=True)
        self.subscription.save()

        self.app = App(
            name='amazon', description='e commerce website',
            subscription=self.subscription, user=self.user
        )
        self.app.save()

        response = self.client.post('/accounts/token', data)
        # print(response.data)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_app_list_authenticated(self):
        response = self.client.get(self.app_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_app_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.app_list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_app_create(self):

        data = {
            'name': 'whatsapp',
            'description': 'social media app'
        }
        response = self.client.post(reverse('app_create'), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_app_detail(self):
        response = self.client.get(reverse('app-detail', kwargs={'pk':self.app.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.app.name, response.data['name'])

    def test_app_update(self):
        data = {
            'name': 'Ali Baba',
            'description': self.app.description
        }
        response = self.client.put(reverse('app-detail', kwargs={'pk':self.app.pk}), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.app.name, response.data['name'])

    def test_update_plan(self):
        plan = Plan(price=10, name='standard')
        plan.save()
        response = self.client.get(reverse('subscription_update', kwargs={
            'pk': self.app.pk, 'plan_pk': plan.pk
        }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(plan.name, response.data['plan']['name'])

    def test_cancel_subcription(self):
        plan = Plan(price=10, name='standard')
        plan.save()
        response = self.client.get(reverse('subscription_cancel', kwargs={
            'pk': self.app.pk
        }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(False, response.data['active'])
