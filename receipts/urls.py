from django.conf.urls import url
from django.shortcuts import redirect

from . import views

urlpatterns = [
    url(r'^$', views.receipts, name='receipts'),
    url(r'^details/(?P<receipt_id>\d+)/$', views.details, name='receipt_details'),
    url(r'^create/$', views.create, name='create_receipt'),
    url(r'^create/(?P<workplace_uuid>.+)/$', views.create, name='create_receipt_with_params'),
    url(r'^delete/$', views.delete, name='delete_receipt'),
    url(r'^update/(?P<receipt_id>.+)/$', views.update, name='update_receipt'),
    url(r'^(?P<workplace_uuid>.+)/(?P<page_num>\d+)/$', views.receipts, name='receipts_with_params'),
]
