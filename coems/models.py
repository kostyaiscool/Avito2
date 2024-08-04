from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=25, null=False, blank=False)
    description = models.CharField(max_length=250, null=True, blank=True)
    icon = models.CharField(max_length=100, default='help', null=True, blank=True)

class Product(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=250, null=True, blank=True)
    image = models.ImageField(upload_to='produx/media/', null=True, blank=True)
    tovar = models.FileField(upload_to='produx/', null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.IntegerField(null=False, blank=False)