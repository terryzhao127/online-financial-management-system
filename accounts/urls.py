from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.custom_login, name='login'),
    url(r'^logout/$', views.custom_logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^password/$', views.change_password, name='change_password'),
]
