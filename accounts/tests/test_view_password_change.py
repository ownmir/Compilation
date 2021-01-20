from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.urls import reverse, resolve
from django.test import TestCase


class PasswordChangeTests(TestCase):
    def setUp(self):
        username = 'neo'
        password = 'mtrxai6ver'
        user = User.objects.create_user(username=username, email='neo@zion.net', password=password)
        url = reverse('standard-accounts:password_change')
        self.client.login(username=username, password=password)
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_correct_view(self):
        view = resolve('/standard-accounts/password_change/')
        self.assertEquals(view.func.view_class, auth_views.PasswordChangeView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordChangeForm)

    def test_form_inputs(self):
        '''
        The view must contain four inputs: csrf, old_password, new_password1, new_password2
        '''
        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, 'type="password"', 3)


class LoginRequiredPasswordChangeTests(TestCase):
    def test_redirection(self):
        url = reverse('standard-accounts:password_change')
        print("url", url)
        login_url = reverse('two_factor:login')
        print("login_url", login_url)
        response = self.client.get(url)
        print("response", response)
        self.assertRedirects(response, f'{login_url}?next={url}')


class PasswordChangeTestCase(TestCase):
    '''
    Base test case for form processing
    accepts a `data` dict to POST to the view.
    '''
    def setUp(self, data={}):
        self.user = User.objects.create_user(username='neo', email='neo@zion.net', password='old_password')
        self.url = reverse('standard-accounts:password_change')
        self.client.login(username='neo', password='old_password')


class SuccessfulPasswordChangeTests(PasswordChangeTestCase):
    def setUp(self):
        self.data = {
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password',
        }
        super().setUp(self.data)
        self.response = self.client.post(self.url, self.data)

    def test_redirection(self):
        """
        A valid form submission should redirect the user
        test accounts.tests.test_view_password_change.SuccessfulPasswordChangeTests.test_redirection
        """
        print("self.response", self.response, "self.data", self.data)

        # self.assertRedirects(self.response, f'{change_url}?next={next_url}')
        self.assertRedirects(self.response, '/standard-accounts/password_change/done/')

    def test_password_changed(self):
        '''
        refresh the user instance from database to get the new password
        hash updated by the change password view.
        '''
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_user_authentication(self):
        '''
        Create a new request to an arbitrary page.
        The resulting response should now have an `user` to its context, after a successful sign up.
        '''
        response = self.client.get(reverse('simply_first'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidPasswordChangeTests(PasswordChangeTestCase):
    def setUp(self, data={}):
        self.data = {
            'old_password': '',
            'new_password1': 'new_password',
            'new_password2': 'new_password',
        }
        super().setUp(self.data)
        self.response = self.client.post(self.url, self.data)

    def test_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_didnt_change_password(self):
        '''
        refresh the user instance from the database to make
        sure we have the latest data.
        '''
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('old_password'))
