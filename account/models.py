from django.db import models

# Create your models here.
# Merchant's Model

class Merchant(models.Model):
    name = models.CharField(max_length=200, blank=True)
    
    seller_id = models.CharField(max_length=20, blank=False, null=True, unique=True)
    owner = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    # profileimg = models.ImageField(upload_to='merchantPics', default='assets/img/placeholder.png')
    
    details = models.TextField(max_length=300, blank=True)
    address = models.TextField(max_length=500, blank=True)
    industry = models.CharField(max_length=50)
    acc_no = models.CharField(max_length=50, null=True)
    acc_name = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=100, blank=True)
    bank = models.CharField(max_length=100, blank=True)
    bvn = models.CharField(max_length=30, null=True)

    # Flutterwave subaccount id
    subAcc_id = models.CharField(max_length=300, blank=False)

    approved = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('date_added')

    class Meta:
        db_table = "Merchant_tb"
        verbose_name = "Merchant"
        verbose_name_plural = "Merchants"


class Customer(models.Model):
    name = models.CharField(max_length=200, blank=False)

    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)
    address = models.TextField(max_length=500, blank=True)
    date_joined = models.DateTimeField(auto_now_add=False, auto_now=True)
    


    def __str__(self):
        return self.name

    class Meta:
        ordering = ('date_joined')

    class Meta:
        db_table = "Customer_tb"
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class Dispatcher(models.Model):
    name = models.CharField(max_length=150, blank=False)
    phoneNumber = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=100, unique=True)
    accNumber = models.CharField(max_length=150, blank=True)
    accName = models.CharField(max_length=150, blank=False)
    bank = models.CharField(max_length=150, blank=False)
    subAcc_id = models.CharField(max_length=300, blank=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=False, auto_now=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ('date_joined')

    class Meta:
        db_table = "Dispatch_tb"
        verbose_name = "Dispatcher"
        verbose_name_plural = "Dispatchers"
