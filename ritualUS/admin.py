from django.contrib import admin
from .models import Product, ProductType, CustomUser, Order, Address, OrderProduct
from django.utils.html import format_html

class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category_display')
    search_fields = ('name',)
    list_filter = ('category',)

    def category_display(self, obj):
        return obj.category.capitalize()
    category_display.short_description = 'Categoría'

admin.site.register(ProductType, ProductTypeAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'is_available', 'product_type')
    search_fields = ('name', 'description',)
    list_filter = ('product_type', 'department', 'section', 'factory')
    list_editable = ('price', 'stock')
    list_per_page = 20
    actions = ['make_available', 'make_unavailable']

    def make_available(self, request, queryset):
        queryset.update(stock=1)
        self.message_user(request, "Los productos seleccionados están ahora disponibles.")
    make_available.short_description = "Marcar productos seleccionados como disponibles"

    def make_unavailable(self, request, queryset):
        queryset.update(stock=0)
        self.message_user(request, "Los productos seleccionados están ahora no disponibles.")
    make_unavailable.short_description = "Marcar productos seleccionados como no disponibles"

    def is_available(self, obj):
        return obj.stock > 0
    is_available.short_description = 'Disponible'

admin.site.register(Product, ProductAdmin)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'dni')
    search_fields = ('username', 'email', 'phone_number', 'dni')
    list_filter = ('is_active', 'is_staff', 'is_superuser')

admin.site.register(CustomUser, CustomUserAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'payment', 'status', 'user', 'shipping_price')
    search_fields = ('id', 'user__username', 'status')
    list_filter = ('status', 'payment')

admin.site.register(Order, OrderAdmin)

class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'city', 'postal_code', 'street', 'number', 'user')
    search_fields = ('country', 'city', 'user__username')
    list_filter = ('country', 'city')

admin.site.register(Address, AddressAdmin)

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product_id', 'quantity', 'unity_price', 'order_product_price')
    search_fields = ('order_id', 'product_id__name')

admin.site.register(OrderProduct, OrderProductAdmin)
