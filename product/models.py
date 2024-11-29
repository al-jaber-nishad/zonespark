from django.db import models
from django.conf import settings
from django.db.models.fields.related import ForeignKey

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(upload_to="category/", blank=True, null=True)
    image = models.ImageField(upload_to="category/", blank=True, null=True)
    parent = ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['-id',]
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=255, null=True, blank=True)
    product_code = models.CharField(max_length=255, null=True, blank=True)
    gtin = models.CharField(max_length=50, null=True, blank=True)
    short_desc = models.TextField(blank=True, null=True)
    full_desc = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    old_price = models.DecimalField(default=0, max_digits=20, decimal_places=2, null=True, blank=True)
    unit_price = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    condition = models.CharField(max_length=10, null=True, blank=True)

    thumbnail = models.ImageField(upload_to="product/", null=True, blank=True)
    rating = models.DecimalField(default=0, max_digits=7, decimal_places=1, null=True, blank=True)
    num_reviews = models.PositiveIntegerField(default=0, null=True, blank=True)

    expire_info = models.TextField(blank=True, null=True)    
    meta_title = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f"{self.id}: {self.name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.BigIntegerField(default=0, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Stocks'
        ordering = ['-id', ]
