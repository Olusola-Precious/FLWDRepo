"""Eecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.contrib import admin
from django.urls import path, include
import os
from django.conf import settings
from django.conf.urls.static import static
from getenv import env

admin.site.site_header = env('APP_NAME') + " Administrator"
admin.site.site_title = env('APP_NAME') + " Administrator"
admin.site.index_title = 'Welcome'


urlpatterns = [
    path("", include('Estore.urls')),
    path("account/", include('account.urls')),
    path("pay/", include('payment.urls')),
    # path('admin/', admin.site.urls),
    path(env('SECRET_ADMIN_URL'), admin.site.urls),
]


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
