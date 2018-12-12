from django.contrib import admin as original_admin
from simple_forum.models import Category, Topic, Post


# Register your models here.
@original_admin.register(Category)
class CategoryAdmin(original_admin.ModelAdmin):
    pass


@original_admin.register(Topic)
class TopicAdmin(original_admin.ModelAdmin):
    pass


@original_admin.register(Post)
class PostAdmin(original_admin.ModelAdmin):
    pass
