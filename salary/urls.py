from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.salary, name='salary'),
    url(r'^details/$', views.salary_details, name='salary_details'),
    url(r'^manage/$', views.salary_manage, name='salary_manage'),
]
