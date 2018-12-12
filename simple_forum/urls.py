from django.urls import path

from simple_forum import views

urlpatterns = [
    # path('forum-admin/', original_admin.site.urls),
    path('', views.simply_first, name='simply_first'),
    path('categories/<int:pk>/', views.category_topics, name='category_topics'),
    path('categories/<int:pk>/new/', views.new_topic, name='new_topic'),
    path('categories/<int:pk>/topics/<int:topic_pk>/', views.PostListView.as_view(), name='topic_posts'),
    path('categories/<int:pk>/topics/<int:topic_pk>/reply/', views.reply_topic, name='reply_topic'),
    path('categories/<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/',
        views.PostUpdateView.as_view(), name='edit_post'),
]