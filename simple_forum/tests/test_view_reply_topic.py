from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from ..models import Category, Post, Topic
from ..views import reply_topic
from ..forms import PostForm


class ReplyTopicTestCase(TestCase):
    """
    Base test case to be used in all `reply_topic` view tests
    """
    def setUp(self):
        self.category = Category.objects.create(name='Django', description='Django board.')
        self.username = 'neo'
        self.password = 'mtrxai6ver'
        user = User.objects.create_user(username=self.username, email='neo@zion.net', password=self.password)
        self.topic = Topic.objects.create(subject='Hello, world', category=self.category, starter=user)
        Post.objects.create(message='Lorem ipsum dolor sit amet', topic=self.topic, created_by=user, updated_by=user)
        self.url = reverse('reply_topic', kwargs={'pk': self.category.pk, 'topic_pk': self.topic.pk})


class LoginRequiredReplyTopicTests(ReplyTopicTestCase):
    # ...
    def setUp(self):
        super().setUp()
        print('self.username', self.username)

    def test_is_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

    def test_is_not_authenticated(self):
        result = self.client.login(username='unknow', password='password')
        self.assertFalse(result)


class ReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()

    def test_status_code(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_view_function(self):
        match_view = resolve('/forum/categories/1/topics/1/reply/')
        self.assertEquals(match_view.func, reply_topic)

    def test_csrf(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        form = response.context.get('form')
        self.assertIsInstance(form, PostForm)

    def test_form_inputs(self):
        """
        The view must contain one input:
        """
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertContains(response, '<input', 1)
        self.assertContains(response, '<textarea', 1)


class SuccessfulReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'message': 'Knock, knock, Neo!'})

    def test_redirection(self):
        url = reverse('topic_posts', kwargs={'pk': self.category.pk, 'topic_pk': self.topic.pk})
        topic_posts_url = '{url}?page=1#2'.format(url=url)
        self.assertRedirects(self.response, topic_posts_url)

    def test_reply_created(self):
        '''
        The total post count should be 2
        The one created in the `ReplyTopicTestCase` setUp
        and another created by the post data in this class
        '''

        self.assertEquals(Post.objects.count(), 2)


class InvalidReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        data = {}
        self.response = self.client.post(self.url, data)

    def test_signup_status_code(self):
        """
        The invalid form must return to the same page
        """
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
