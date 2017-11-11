from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.get_page, name='salary'),
    url(r'upload/$', views.upload_file, name='upload'),
    url(r'details/$', views.details, name='salary_details')
]
