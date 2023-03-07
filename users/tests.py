from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):

    def setUp(self):
        self.data = {
            'first_name': 'Andrii', 'last_name': 'Sky',
            'username': 'andrii', 'email': 'andrii@gmail.ru',
            'password1': '12345678pP', 'password2': '12345678pP',
        }
        self.path = reverse('users:register')

    def test_01_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Registration')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_02_user_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())  # there was no username BEFORE the request
        response = self.client.post(self.path, self.data)

        # check creating of user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())  # there was no username AFTER the request

        # check creating of email verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(email_verification.first().expiration.date(),
                         (now() + timedelta(hours=48)).date())

    def test_03_user_registration_post_error(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'A user with that username already exists.', html=True)


class UserLoginViewTestCase(TestCase):

    def setUp(self):
        self.data = {
            'first_name': 'Andrii', 'last_name': 'Sky',
            'username': 'andrii', 'email': 'andrii@gmail.ru',
            'password1': '12345678pP', 'password2': '12345678pP',
            'password': '12345678pP',
        }
        self.path = reverse('users:login')

    def test_01_login_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Login')
        self.assertTemplateUsed(response, 'users/login.html')

    def test_02_user_login_post_error(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())  # there was no username BEFORE the request

        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response,
                            'Please enter a correct username and password. Note that both fields may be case-sensitive.',
                            html=True)

    def test_03_user_login_post_success(self):
        User.objects.create(username=self.data['username'], password=self.data['password'])
        self.assertTrue(User.objects.filter(username=self.data['username']).exists())

        response = self.client.post(
            self.path,
            data={
                'username': self.data['username'],
                'password': self.data['password'],
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        """ finish later """





