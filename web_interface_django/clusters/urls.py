from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^clusters', views.cluster_list, name = 'clusters')
]