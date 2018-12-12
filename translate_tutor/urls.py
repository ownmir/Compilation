from django.urls import path
from translate_tutor import views

urlpatterns = [
    path('', views.translate_tutor, name='translate_tutor'),
    path('6/', views.translate_tutor6, name='translate_tutor6'),
    path('7/', views.translate_tutor7, name='translate_tutor7'),
]