from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from simple_forum import urls as forum_urls
from accounts import urls as accounts_urls
from translate_tutor import urls as translate_tutor_urls
from captcha import urls as captcha_urls

from search import views as search_views
from blog import views as blog_views

urlpatterns = [
    url(r'^django-admin/', admin.site.urls),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^forum/', include(forum_urls)),
    url(r'^accounts/', include(accounts_urls)),
    # path('captcha/', include('captcha.urls')),
    path('captcha/', include(captcha_urls)),

    url(r'^search/$', search_views.search, name='search'),
    url(r'^index/indent/$', blog_views.indent, name='indent'),
    url(r'^translate/', include(translate_tutor_urls)),


    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(translate_tutor_urls)),
    url(r'^wt/', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
