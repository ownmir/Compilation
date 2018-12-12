from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Category, Post, Topic
from ..views import PostListView


class TopicPostsTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Django', description='Django board.')
        user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        topic = Topic.objects.create(subject='Hello, world', category=category, starter=user)
        Post.objects.create(message='Lorem ipsum dolor sit amet', topic=topic, created_by=user, updated_by=user)
        url = reverse('topic_posts', kwargs={'pk': category.pk, 'topic_pk': topic.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/forum/categories/1/topics/1/')
        self.assertEquals(view.func.view_class, PostListView)
