from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^choice/(?P<url_id>[0-9]+)/tags/(?P<tag>[А-Яа-яёЁA-Za-z]+)/$', views.texts_tag, name='texts_tag'),
    url(r'^choice/(?P<url_id>[0-9]+)/clusters/(?P<cluster_id>[0-9]+)/$', views.texts_cluster, name='texts_cluster'),
    url(r'^choice/(?P<url_id>[0-9]+)/texts/(?P<text_id>[0-9]+)/$', views.text_info, name='text_info'),
    url(r'^urls/', views.urls, name='urls')
]