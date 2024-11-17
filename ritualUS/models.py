# ritualUS/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from enum import Enum

class Category(Enum):
    CANDLE = "candle"
    AROMATHERAPY = "aromatherapy"
    JEWELRY = "jewelry"
    DECORATION = "decoration"
    
    @classmethod
    def choices(enum):
        return [(i.value, i.name) for i in enum]

class ProductType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField()
    category = Category.choices()

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField()
    category = Category.choices()
    description = models.CharField()
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    image = models.ImageField()
    stock = models.IntegerField()
    is_available = models.BooleanField()
    department = models.CharField(blank=True, null=True)
    section = models.CharField(blank=True, null=True)
    factory = models.CharField(blank=True, null=True)
    product_type = models.OneToOneField(ProductType, on_delete=models.CASCADE)

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    dni = models.CharField(max_length=9, unique=True, null=False)

    def __str__(self):
        return self.username
