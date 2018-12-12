# from django.test import TestCase
# from django.urls import reverse, resolve
# from ..views import simply_first, category_topics, new_topic
# from ..models import Category, Topic, Post
# from django.contrib.auth.models import User
# from ..forms import NewTopicForm
#
#
# # Create your tests here.
# class FirstTests(TestCase):
#     def setUp(self):
#         self.category = Category.objects.create(name="Django", description='Django category.')
#         url = reverse('simply_first')
#         self.response = self.client.get(url)
#
#     def test_simply_first_view_status_code(self):
#         self.assertEquals(self.response.status_code, 200)
#
#     def test_simply_url_resolve_first_view(self):
#         match_view = resolve('/forum/')
#         self.assertEquals(match_view.func, simply_first)
#
#     def test_simply_first_view_contain_link_to_topic_page(self):
#         category_topics_url = reverse('category_topics', kwargs={'pk': self.category.pk})
#         self.assertContains(self.response, 'href="{0}"'.format(category_topics_url))
#
#
# #
# class CategoryTopicsTests(TestCase):
#     def setUp(self):
#         Category.objects.create(name="Django", description='Django category.')
#
#     def test_category_topics_view_success_status_code(self):
#         url = reverse('category_topics', kwargs={'pk': 1})
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 200)
#
#     def test_category_topics_view_not_found_status_code(self):
#         url = reverse('category_topics', kwargs={'pk': 99})
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 404)
#
#     def test_category_topics_url_resolves_category_topics_view(self):
#         match_view = resolve('/forum/categories/1/')
#         self.assertEquals(match_view.func, category_topics)
#
#     def test_category_topics_view_contains_navigation_links(self):
#         category_topics_url = reverse('category_topics', kwargs={'pk': 1})
#         response = self.client.get(category_topics_url)
#         first_page_url = reverse('simply_first')
#         new_topic_url = reverse('new_topic', kwargs={'pk': 1})
#         self.assertContains(response, 'href="{0}"'.format(first_page_url))
#         self.assertContains(response, 'href="{0}"'.format(new_topic_url))
#
#
# class NewTopicTests(TestCase):
#     def setUp(self):
#         Category.objects.create(name='Flowers', description='About children')
#         User.objects.create_user(username='bruce', email='bruce@willis.com', password='diehard')
#
#     def test_new_topic_view_success_status_code(self):
#         url = reverse('new_topic', kwargs={'pk': 1})
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 200)
#
#     def test_new_topic_view_not_found_status_code(self):
#         url = reverse('new_topic', kwargs={'pk': 99})
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 404)
#
#     def test_new_topic_url_resolves_new_topic_view(self):
#         match_view = resolve('/forum/categories/1/new/')
#         self.assertEquals(match_view.func, new_topic)
#
#     def test_new_topic_view_contains_link_back_to_category_topics_view(self):
#         new_topic_url = reverse('new_topic', kwargs={'pk': 1})
#         category_topics_url = reverse('category_topics', kwargs={'pk': 1})
#         response = self.client.get(new_topic_url)
#         self.assertContains(response, 'href="{0}"'.format(category_topics_url))
#
#     def test_csrf(self):
#         url = reverse('new_topic', kwargs={'pk': 1})
#         response = self.client.get(url)
#         self.assertContains(response, 'csrfmiddlewaretoken')
#
#     def test_new_topic_valid_post_data(self):
#         url = reverse('new_topic', kwargs={'pk': 1})
#         data = {'subject': 'subject one', 'message': 'Body of message'}
#         response = self.client.post(url, data)
#         self.assertTrue(Topic.objects.exists())
#         self.assertTrue(Post.objects.exists())
#
#     def test_new_topic_invalid_post_data(self):
#         url = reverse('new_topic', kwargs={'pk': 1})
#         response = self.client.post(url, {})
#         form = response.context.get('form')
#         self.assertEquals(response.status_code, 200)
#         self.assertTrue(form.errors)
#
#     def test_new_topic_contains_form(self):
#         url = reverse('new_topic', kwargs={'pk': 1})
#         response = self.client.get(url)
#         form = response.context.get('form')
#         self.assertIsInstance(form, NewTopicForm)
#
#     def test_new_topic_invalid_post_data_empty_fields(self):
#         url = reverse('new_topic', kwargs={'pk': 1})
#         data = {'subject': '', 'message': ''}
#         response = self.client.post(url, data)
#         self.assertEquals(response.status_code, 200)
#         self.assertFalse(Topic.objects.exists())
#         self.assertFalse(Post.objects.exists())
