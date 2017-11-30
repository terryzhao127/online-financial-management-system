from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.tables, name='tables'),
    url(r'details/(?P<table_id>\d+)/$', views.details, name='table_details'),
    url(r'^create/$', views.create, name='create_table'),
    url(r'create/(?P<workplace_uuid>.+)/$', views.create, name='create_table_with_params'),
    url(r'delete/$', views.delete, name='delete_table'),
    url(r'update/(?P<table_id>\d+)/$', views.update, name="update_table"),
    url(r'^(?P<workplace_uuid>.+)/(?P<page_num>\d+)/$', views.tables, name='tables_with_params'),
]
