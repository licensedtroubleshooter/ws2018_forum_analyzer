from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^choice', views.choice, name = 'choice'),
    url(r'^', views.choice, name = 'choice')
]