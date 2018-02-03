from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^choice/(?P<url_id>[0-9]+)/clusters', views.cluster_list, name = 'clusters')
]