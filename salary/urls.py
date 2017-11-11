from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.salary, name='salary'),
    url(r'upload/$', views.upload, name='upload'),
    url(r'details/$', views.details, name='salary_details')
]
