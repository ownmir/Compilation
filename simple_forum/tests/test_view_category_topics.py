from django.test import TestCase
from django.urls import reverse, resolve
from ..views import category_topics
from ..models import Category


#
class CategoryTopicsTests(TestCase):
    def setUp(self):
        Category.objects.create(name="Django", description='Django category.')

    def test_category_topics_view_success_status_code(self):
        url = reverse('category_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_category_topics_view_not_found_status_code(self):
        url = reverse('category_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_category_topics_url_resolves_category_topics_view(self):
        match_view = resolve('/forum/categories/1/')
        self.assertEquals(match_view.func, category_topics)

    def test_category_topics_view_contains_navigation_links(self):
        category_topics_url = reverse('category_topics', kwargs={'pk': 1})
        response = self.client.get(category_topics_url)
        first_page_url = reverse('simply_first')
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        self.assertContains(response, 'href="{0}"'.format(first_page_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))
