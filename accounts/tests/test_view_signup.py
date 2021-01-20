from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from ..forms import SignUpForm  # add email
from django.urls import reverse
from django.urls import resolve
from django.test import TestCase
from ..views import signup
from captcha.models import CaptchaStore


# Create your tests here.
class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('standard-accounts:signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/standard-accounts/signup/')
        self.assertEquals(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        """
        The view must contain five input:
        """
        self.assertContains(self.response, '<input', 7)
        self.assertContains(self.response, 'type="text"', 2)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignupTests(TestCase):
    def setUp(self):
        url = reverse('standard-accounts:signup')
        captcha_count = CaptchaStore.objects.count()
        self.failUnlessEqual(captcha_count, 0)

        captcha = CaptchaStore.objects.get(hashkey=CaptchaStore.generate_key())
        captcha_count = CaptchaStore.objects.count()
        self.failUnlessEqual(captcha_count, 1)
        data = {
            'username': 'neo',
            'email': 'neo@zion.net',
            'password1': 'mtrxai6ver',
            'password2': 'mtrxai6ver',
            # 'captcha_0': 'dummy-value',
            'captcha_0': captcha.hashkey,
            # 'captcha_1': 'PASSED'
            'captcha_1': captcha.response
        }
        self.response = self.client.post(url, data)
        self.simple_forum_url = reverse('two_factor:profile')

    def test_redirection(self):
        """
        The valid form should redirect the user to the first page of the forum
        """
        self.assertRedirects(self.response, self.simple_forum_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        """
        The resulting response has "user" in its context
        """
        response = self.client.get(self.simple_forum_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignupTests(TestCase):
    def setUp(self):
        url = reverse('standard-accounts:signup')
        data = {}
        self.response = self.client.post(url, data)

    def test_signup_status_code(self):
        """
        The invalid form must return to the same page
        """
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())
