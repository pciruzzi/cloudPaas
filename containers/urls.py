from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^run/(?P<container_id>[0-9]+)/$', views.run, name='run'),
]
