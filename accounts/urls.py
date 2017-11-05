from django.conf.urls import url
from . import views

import django.contrib.auth.views as auth_views

urlpatterns = [
    url(r'^login/$', views.custom_login, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'accounts/logout.html'}, name='logout'),
    url(r'^password/$', views.change_password, name='change_password'),
]
