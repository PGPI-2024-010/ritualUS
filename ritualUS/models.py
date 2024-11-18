# ritualUS/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from enum import Enum

class Payment(Enum):
    CASH = "cash"
    CREDIT_CARD = "credit card"
    
    @classmethod
    def choices(enum):
        return [(i.value, i.name) for i in enum]

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
    name = models.CharField(max_length=100)
    category = Category.choices()

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    category = Category.choices()
    description = models.CharField(max_length=500)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    image = models.ImageField()
    stock = models.IntegerField()
    is_available = models.BooleanField()
    department = models.CharField(max_length=100, blank=True, null=True)
    section = models.CharField(max_length=100, blank=True, null=True)
    factory = models.CharField(max_length=100, blank=True, null=True)
    product_type = models.OneToOneField(ProductType, on_delete=models.CASCADE)

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.CharField()
    city = models.CharField
    postal_code = models.CharField()
    street = models.CharField()
    number = models.IntegerField
    apartment_number = models.CharField()

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField()
    surname = models.CharField()
    dni = models.CharField()
    username = models.CharField()
    password = models.CharField()
    email = models.EmailField()
    telephone_number = models.CharField()
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    payment = Payment.choices()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class OrderProduct(models.Model):
    order_id = models.OneToOneField(Order, on_delete=models.CASCADE)
    product_id = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unity_price = models.FloatField()

    def __str__(self):
        return self.title
    
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    dni = models.CharField(max_length=9, unique=True, null=False)

    def __str__(self):
        return self.username
