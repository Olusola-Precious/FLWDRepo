from django import urls
from django.urls import path
from .import views


urlpatterns = [
    path("", views.index, name="home"),
    path("store", views.store, name="store"),
    path("product", views.product, name="product"),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    

]
