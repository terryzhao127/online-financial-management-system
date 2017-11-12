from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.receipts, name='receipts'),
    url(r'^details/$', views.details, name='receipt_details'),
    url(r'^create/', views.create, name='create_receipt')
]
