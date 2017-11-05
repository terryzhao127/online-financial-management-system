from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^', views.error_404, name='error_404')
]
