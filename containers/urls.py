from django.conf.urls import url
from . import views

urlpatterns = [
   	url(r'^$', views.index, name='index'),
	url(r'^create/$', views.create, name='create'),
	#url(r'^run/(?P<container_id>[0-9]+)/$', views.run, name='run'),
	#url(r'^stop/$', views.stop, name='stop'),
	url(r'^change/$', views.change, name='change'),
	url(r'^delete/$', views.delete, name='delete'),
	url(r'^backup/$', views.backup, name='backup'),
]
