from django.db import migrations
from datetime import date


def populate_orders(apps, schema_editor):
    CustomUser = apps.get_model('ritualUS', 'CustomUser')
    Product = apps.get_model('ritualUS', 'Product')
    Order = apps.get_model('ritualUS', 'Order')
    OrderProduct = apps.get_model('ritualUS', 'OrderProduct')
    Address = apps.get_model('ritualUS', 'Address')

    # Seleccionar un usuario (el primero creado)
    user = CustomUser.objects.first()
    if not user:
        print("No se encontró ningún usuario. Asegúrate de crear usuarios antes.")
        return

    # Crear una dirección para el usuario
    address = Address.objects.create(
        country="España",
        city="Sevilla",
        postal_code="41001",
        street="Calle Falsa",
        number=123,
        apartment_number="1A",
        user=user
    )

    # Crear una orden para el usuario y asociarle la dirección
    orderC = Order.objects.create(
        id=1,
        date=date.today(),
        payment='credit card',
        user=user,
        address=address
    )

    # Seleccionar productos y definir cantidades
    productos = [
        {"product_id": 1, "quantity": 2},
        {"product_id": 2, "quantity": 3},
        {"product_id": 3, "quantity": 1},
        {"product_id": 4, "quantity": 5},
    ]

    # Crear las relaciones entre la orden y los productos
    for item in productos:
        try:
            productoC = Product.objects.get(id=item["product_id"])
            OrderProduct.objects.create(
                order_id=orderC,  # Usar directamente el objeto de la orden
                product_id=productoC,  # Usar directamente el objeto del producto
                quantity=item["quantity"],
                unity_price=productoC.price
            )
        except Product.DoesNotExist:
            print(f"Producto con ID {item['product_id']} no existe.")
            continue

    print(f"Orden creada correctamente con ID {
          orderC.id} y sus productos asociados.")


class Migration(migrations.Migration):

    dependencies = [
        # Cambia el nombre si es necesario
        ('ritualUS', '0003_alter_product_image'),
    ]

    operations = [
        # Ejecuta la función para poblar órdenes
        migrations.RunPython(populate_orders),
    ]
