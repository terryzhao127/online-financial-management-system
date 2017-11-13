from django.conf.urls import url
from django.shortcuts import redirect

from . import views

urlpatterns = [
    url(r'^$', lambda r: redirect('/receipts/1/')),
    url(r'^(?P<page_num>\d+)/$', views.receipts, name='receipts'),
    url(r'^details/(?P<receipt_id>\d+)/$', views.details, name='receipt_details'),
    url(r'^create/$', views.create, name='create_receipt'),
    url(r'^delete/$', views.delete, name='delete_receipt'),
]
