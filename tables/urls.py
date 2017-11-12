from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.tables, name='tables'),
    url(r'details/$', views.details, name='table_details'),
    url(r'upload/$', views.upload, name='upload')
]
