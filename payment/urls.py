from django import urls
from django.urls import path
from .import views


urlpatterns = [
    path("", views.pay, name="pay"),
    path("confirm", views.confirm, name="confirm"),
    path("verify", views.verify, name="verify"),
]
