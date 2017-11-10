from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.get_page, name='companies'),
    # url(r'^create/page/$', TemplateView.as_view(template_name="companies/create_company.html"),
        # name='create_company_page'),
    url(r'^create/$', views.create_company, name='create_company'),
]
