from django.conf.urls import url
from . import views
from django.shortcuts import redirect

urlpatterns = [
    url(r'^$', lambda r: redirect('/companies/1+1/')),
    url(r'^(?P<workplaces_page_num>\d+)\+(?P<owned_companies_page_num>\d+)/$', views.companies, name='companies'),
    url(r'^create/$', views.create, name='create_company'),
    url(r'^join/$', views.join, name='join_company'),
    url(r'^delete/$', views.delete, name='delete_company'),
    url(r'^fire/$', views.fire_staff, name='fire_employee'),
    url(r'^quit/$', views.leave, name='quit_company'),
    url(r'^manage/(?P<company_uuid>.+)/$', views.render_staff_page, name='manage_staff'),
    url(r'^update/(?P<company_uuid>.+)/$', views.update, name='update_company'),
    url(r'^details/(?P<company_uuid>.+)/$', views.details, name='company_details'),
]
