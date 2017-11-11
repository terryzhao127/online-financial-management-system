from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.get_page, name='companies'),
    url(r'^create/$', views.create_company, name='create_company'),
    url(r'^join/$', views.join_company, name='join_company'),
    url(r'^delete/$', views.delete_company, name='delete_company'),
]
