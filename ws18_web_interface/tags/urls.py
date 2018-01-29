from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^tags', views.tag_list, name = 'tags')
]