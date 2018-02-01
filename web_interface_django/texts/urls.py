from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^tags/(?P<tag>[А-Яа-яёЁA-Za-z]+)/$', views.texts_tag, name='texts_tag'),
    url(r'^clusters/(?P<cluster_id>[0-9]+)/$', views.texts_cluster, name='texts_cluster'),
    url(r'^texts/(?P<text_id>[0-9]+)/$', views.text_info, name='text_info')
]