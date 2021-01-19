from django.contrib import admin
from .models import Merchant, Customer, Dispatcher

# Register your models here.
admin.site.register(Merchant)
admin.site.register(Customer)
admin.site.register(Dispatcher)
