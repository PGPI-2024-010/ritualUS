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


class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_DELIVERY = "in delivery"
    DELIVERED = "delivered"

    @classmethod
    def choices(enum):
        return [(i.value, i.name) for i in enum]


class ProductType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Nombre del tipo de producto")
    category = models.CharField(
        max_length=50, choices=Category.choices(), default=Category.CANDLE.value, verbose_name="Categoría")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Tipo de Producto"
        verbose_name_plural = "Tipos de Producto"


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Nombre del producto")
    description = models.CharField(max_length=500, verbose_name="Descripción del producto")
    price = models.FloatField(verbose_name="Precio")
    discount_price = models.FloatField(blank=True, null=True, verbose_name="Precio con descuento")
    image = models.ImageField(verbose_name="Imagen")
    stock = models.IntegerField(verbose_name="Stock")
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name="Departamento")
    section = models.CharField(max_length=100, blank=True, null=True, verbose_name="Sección")
    factory = models.CharField(max_length=100, blank=True, null=True, verbose_name="Fabricante")
    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name="product", verbose_name="Tipo de producto")

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ['name']
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    @property
    def is_available(self):
        return self.stock > 0

    def __str__(self):
        return str(self.name)


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=100, verbose_name="País")
    city = models.CharField(max_length=100, verbose_name="Ciudad")
    postal_code = models.CharField(max_length=50, verbose_name="Código Postal")
    street = models.CharField(max_length=100, verbose_name="Calle")
    number = models.IntegerField(verbose_name="Número")
    apartment_number = models.CharField(max_length=50, null=True, verbose_name="Número de apartamento")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="address", null=True, verbose_name="Usuario")
    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de la orden")
    payment = models.CharField(max_length=100, choices=Payment.choices(), verbose_name="Método de pago")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="order", blank=True, null=True, verbose_name="Usuario")
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="order", blank=True, null=True, verbose_name="Dirección")
    status = models.CharField(max_length=50, choices=OrderStatus.choices(),
                              default=OrderStatus.PENDING.value, verbose_name="Estado")
    shipping_price = models.FloatField(default=5.0, verbose_name="Precio de envío")

    class Meta:
        verbose_name = "Orden"
        verbose_name_plural = "Órdenes"



class OrderProduct(models.Model):
    order_id = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_product", verbose_name="Orden")
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_product", verbose_name="Producto")
    quantity = models.IntegerField(verbose_name="Cantidad")
    unity_price = models.FloatField(verbose_name="Precio unitario")

    @property
    def order_product_price(self):
        return self.quantity*self.unity_price
    
    class Meta:
        verbose_name = "Orden de producto"
        verbose_name_plural = "Órdenes de producto"


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    dni = models.CharField(max_length=9, null=False, blank=False)

    def __str__(self):
        return str(self.username)
