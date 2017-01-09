from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signUp/$',views.signUp,name='signUp'),
	url(r'^login/$', auth_views.login,{'template_name': 'authentication/login.html'}, name='login'),
	url(r'^logout/$', auth_views.logout,{'template_name': 'authentication/logout.html'},name='logout'),
]
