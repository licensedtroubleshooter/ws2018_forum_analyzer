from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^choice/(?P<url_id>[0-9]+)', views.choice, name = 'choice'),
    url(r'^', views.go_url, name = 'index')
]