from django.test import TestCase
from django.urls import reverse, resolve
from ..views import simply_first
from ..models import Category


# Create your tests here.
class FirstTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Django", description='Django category.')
        url = reverse('simply_first')
        self.response = self.client.get(url)

    def test_simply_first_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_simply_url_resolve_first_view(self):
        match_view = resolve('/forum/')
        self.assertEquals(match_view.func, simply_first)

    def test_simply_first_view_contain_link_to_topic_page(self):
        category_topics_url = reverse('category_topics', kwargs={'pk': self.category.pk})
        self.assertContains(self.response, 'href="{0}"'.format(category_topics_url))
