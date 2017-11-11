from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.receipts, name='receipts'),
    url(r'^details/$', views.receipt_details, name='receipt_details'),
]
