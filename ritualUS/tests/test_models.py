from django.test import TestCase
from ritualUS.models import *

class ModelTests(TestCase):
    def test_create_objects(self):
        product = Product.objects.create(name='Test product', stock=10, price=50, product_type=ProductType.objects.first())
        order = Order.objects.create(payment='cash')
        address = Address.objects.create(country="Pais", city="Ciudad", postal_code="12345", street="Calle", number=1)
        order_product = OrderProduct.objects.create(quantity=4,unity_price=20,order_id=order,product_id=product)
        self.assertTrue(product.is_available)
        self.assertEqual(order.status,OrderStatus.PENDING.value)
        self.assertEqual(order_product.order_product_price,80)
        self.assertIsNotNone(address.id)