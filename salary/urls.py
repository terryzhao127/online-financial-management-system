from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.salary, name='salary'),
    url(r'details/(?P<salary_id>\d+)/$', views.details, name='salary_details'),
    url(r'create/$', views.create, name='create_salary'),
    url(r'create/(?P<company_uuid>.+)/$', views.create, name='create_salary_with_params'),
    url(r'delete/$', views.delete, name='delete_salary'),
    url(r'update/(?P<salary_id>\d+)$', views.update, name="update_salary"),
    url(r'^(?P<company_uuid>.+)/(?P<page_num>\d+)/$', views.salary, name='salary_with_params'),
]
