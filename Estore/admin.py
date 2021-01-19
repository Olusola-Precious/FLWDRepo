from django.contrib import admin
from .models import Product, Store_Category, ProductCategory, Cart
# Register your models here.
admin.site.register(Product)
admin.site.register(Store_Category)
admin.site.register(ProductCategory)
admin.site.register(Cart)
