from django.core import mail
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase


class PasswordResetMailTests(TestCase):
    def setUp(self):
        email = 'neo@zion.net'
        User.objects.create_user(username='neo', email=email, password='mtrxai6ver')
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': email})
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual('[Forum] Please reset your password', self.email.subject)

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('neo', self.email.body)
        self.assertIn('neo@zion.net', self.email.body)

    def test_email_to(self):
        self.assertEqual(['neo@zion.net', ], self.email.to)