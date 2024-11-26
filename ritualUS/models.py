# ritualUS/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from enum import Enum
from django.conf import settings


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
    category = models.CharField(
        max_length=50, choices=Category.choices(), default=Category.CANDLE.value)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    image = models.ImageField()
    stock = models.IntegerField()
    department = models.CharField(max_length=100, blank=True, null=True)
    section = models.CharField(max_length=100, blank=True, null=True)
    factory = models.CharField(max_length=100, blank=True, null=True)
    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name="product")

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ['name']

    @property
    def is_available(self):
        return self.stock > 0

    def __str__(self):
        return str(self.name)


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    number = models.IntegerField()
    apartment_number = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="address")


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    payment = models.CharField(max_length=100, choices=Payment.choices())
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="order")
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="order")


class OrderProduct(models.Model):
    order_id = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_product")
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_product")
    quantity = models.IntegerField()
    unity_price = models.FloatField()


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    dni = models.CharField(max_length=9, null=False, blank=False)

    def __str__(self):
        return str(self.username)
