from django.test import TestCase
from django.urls import reverse, resolve
from .views import indent


# Задокументировал! так как убрал из testwagtail/urls url(r'^admin/', include(wagtailadmin_urls)),
# class IndentTests(TestCase):
#     def test_indent_view_status_code(self):
#         url = reverse('indent')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#
#     def test_indent_url_resolves_indent_view(self):
#         match_view = resolve('/index/indent/')
#         self.assertEqual(match_view.func, indent)

# TODO search
