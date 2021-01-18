from django.db import models

# Create your models here.
# Merchant's Model

class Merchant(models.Model):
    merchant_name = models.CharField(max_length=200, blank=True)
    
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

    approved = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.merchant_name

    class Meta:
        ordering = ('date_added')

    class Meta:
        db_table = "Merchant_tb"
        verbose_name = "Merchant"
        verbose_name_plural = "Merchants"
