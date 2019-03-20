"""online_financial_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', lambda r: redirect('/index/')),
    url(r'^index/', include('index.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^companies/', include('companies.urls')),
    url(r'^info/', include('info.urls')),
    url(r'^receipts/', include('receipts.urls')),
    url(r'^tables/', include('tables.urls')),
    url(r'^tax/', include('tax.urls')),
    url(r'^salary/', include('salary.urls')),
    url(r'^admin/', admin.site.urls),
]

# For serving static files even not in debug mode...
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
elif getattr(settings, 'FORCE_SERVE_STATIC', False):
    settings.DEBUG = True
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    settings.DEBUG = False

handler404 = 'errors.views.error_404'
handler403 = 'errors.views.error_403'
