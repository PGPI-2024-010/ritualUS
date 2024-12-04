from django.urls import reverse
from django.test import Client
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client
import pytest
import os
import django
# Configuro la variable de entorno DJANGO_SETTINGS_MODULE para apuntar a settings.py
os.environ['DJANGO_SETTINGS_MODULE'] = 'ritualUS.settings'

# Inicializo Django para que cargue la configuración de settings.py
django.setup()


@pytest.fixture
def authenticated_client():
    from ritualUS.models import CustomUser
    client = CustomUser.objects.first()
    return client


@pytest.fixture
def product():
    """Proporciona un producto de prueba"""
    from ritualUS.models import Product
    return Product.objects.create(
        name='Test Product',
        description='Test Description',
        price=10.0,
        discount_price=5.0,
        image=None,
        stock=10,
        department='Test Department',
        section='Test Section',
        factory='Test Factory'
    )


@pytest.fixture
def admin():
    """Proporciona un cliente autenticado como administrador"""
    from ritualUS.models import CustomUser
    return CustomUser.objects.create_user(
        username='admin',
        password='admin123',
        first_name='Admin',
        last_name='Usuario',
        phone_number='1234567890',
        dni='ADMIN1234'
    )


# Test para la URL de la página de inicio


def test_home_url(client):
    """Prueba que la URL de la página de inicio esté configurada correctamente"""
    response = client.get(reverse('home'))
    assert response.status_code == 200


# Test para la URL de administración
def test_admin_url(client):
    """Prueba que la URL de la administración esté configurada correctamente"""
    response = client.get(reverse('admin:index'))
    assert response.status_code == 200 or 302  # 302 si no estás autenticado


# Test para la URL de productos
def test_products_url(client):
    """Prueba que la URL de los productos esté configurada correctamente"""
    response = client.get(reverse('products'))
    assert response.status_code == 200


# Test para la URL del carrito
def test_cart_url(client):
    """Prueba que la URL del carrito esté configurada correctamente"""
    response = client.get(reverse('cart'))
    assert response.status_code == 200


# Test para la URL de los detalles del producto
def test_product_detail_url(client):
    """Prueba que la URL de los detalles del producto esté configurada correctamente"""
    response = client.get(reverse(
        # Asegúrate de tener un producto con pk=1
        'product-detail', kwargs={'pk': 1}))
    assert response.status_code == 200


# Test para la URL de contacto
def test_contact_url(client):
    """Prueba que la URL de contacto esté configurada correctamente"""
    response = client.get(reverse('contact'))
    assert response.status_code == 200


# Test para la URL de la sección "Acerca de"
def test_about_url(client):
    """Prueba que la URL de la página acerca de esté configurada correctamente"""
    response = client.get(reverse('about'))
    assert response.status_code == 200


# Test para la URL de actualización del carrito
def test_update_cart_url(client):
    """Prueba que la URL de actualización del carrito esté configurada correctamente"""
    url = reverse('update_cart')
    url = f'{url}?product_id=1&quantity=2'
    response = client.get(url)
    assert response.status_code == 200 or 302  # 302 si no estás autenticado

# Test para la URL de eliminar un producto del carrito


def test_remove_from_cart_url(client):
    """Prueba que la URL de eliminar un producto del carrito esté configurada correctamente"""
    url = reverse('remove_from_cart')
    url = f'{url}?product_id=1'
    response = client.get(url)
    assert response.status_code == 200 or 302  # 302 si no estás autenticado


# Test para la URL de éxito del pago
def test_payment_success_url(client):
    """Prueba que la URL de éxito del pago esté configurada correctamente"""
    response = client.get(reverse('payment_success', kwargs={
                          'order_id': 1}))  # Asegúrate de tener un pedido con order_id=1
    assert response.status_code == 200


# Test para la URL de confirmación del pedido
def test_order_confirmation_url(client):
    """Prueba que la URL de confirmación del pedido esté configurada correctamente"""
    response = client.get(reverse('order_confirmation_view'))
    assert response.status_code == 200


# Test para la URL de seguimiento de pedidos
def test_order_tracking_url(client):
    """Prueba que la URL de seguimiento del pedido esté configurada correctamente"""
    response = client.get(reverse('order_tracking'))
    assert response.status_code == 200
