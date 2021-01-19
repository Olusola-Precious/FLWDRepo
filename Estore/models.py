from account.models import Merchant
from django.db import models
from account.models import Merchant, Customer


# Create your models here.
class Store_Category(models.Model):
    # thum_img = models.ImageField(upload_to='StorePics', default='assets/img/placeholder.png')
    name = models.CharField(max_length=50, null=False, blank=False)
    merchant_id = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=True)
    industry = models.CharField(max_length=80, null=False)
    date_added = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('date_added')

    class Meta:
        db_table = "StoreCategory_tb"
        verbose_name = "Store Category"
        verbose_name_plural = "Store Categories"


class ProductCategory(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    thum_img = models.ImageField(
        upload_to='categoryPics', default='assets/img/productCategoryPlaceholder.jpg', blank=True)
    date_added = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('date_added')

    class Meta:
        db_table = "ProductCat_tb"
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"


class Product(models.Model):
    Shop = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    store_id = models.ForeignKey(Store_Category, on_delete=models.CASCADE)
    category_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False, blank=False)
    Description = models.TextField(max_length=800, null=True)
    prodImgMain = models.ImageField(upload_to='productPics', default='assets/img/prodPlaceholder.jpg', blank=False)
    prodImg2 = models.ImageField(upload_to='productPics', default='assets/img/prodPlaceholder.jpg', blank=True, null=True)
    prodImg3 = models.ImageField(upload_to='productPics',
                                 default='assets/img/prodPlaceholder.jpg', blank=True, null=True)
    prodImg4 = models.ImageField(
        upload_to='productPics', default='assets/img/prodPlaceholder.jpg', blank=True, null=True)
    discount = models.CharField(max_length=12, null=True)
    price = models.CharField(max_length=12, null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('date_added')

    class Meta:
        db_table = "Product_tb"
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Cart(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.CharField(max_length=50, null=False, blank=False)
    cleared = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Cart-" + str(self.date_added)

    class Meta:
        ordering = ('date_added')

    class Meta:
        db_table = "Cart_tb"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"



    
