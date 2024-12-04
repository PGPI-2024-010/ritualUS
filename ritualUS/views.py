
from django.views.generic import ListView, DetailView
from .models import Product, Category, OrderProduct, Order, Address, Payment, OrderStatus, ProductType
from django.contrib.auth.decorators import login_required
from .forms import CustomSignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
import os
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from dotenv import load_dotenv
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta

stripe.api_key = settings.STRIPE_API_KEY


class Home(ListView):
    template_name = 'index.html'
    queryset = Product.objects.filter(stock__gt=0)
    context_object_name = 'products'


@login_required
def profile_view(request):
    user = request.user
    if request.method == "POST":
        user = request.user
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone_number')
        user.save()
        messages.success(request, "Perfil actualizado")
        return redirect('account_logout')
    return render(request, 'profile.html', {'user': user})


def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo usuario
            # Redirige al login o a la página que prefieras
            return redirect('account_login')
    else:
        form = CustomSignupForm()

    return render(request, 'signup.html', {'form': form})


class ProductListView(ListView):
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects.all()

        # Filtrar por categoría (si existe)
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(product_type_id=category_id)

        # Filtrar por departamento
        department = self.request.GET.get('department')
        if department:
            queryset = queryset.filter(department__icontains=department)

        # Filtrar por sección
        section = self.request.GET.get('section')
        if section:
            queryset = queryset.filter(section__icontains=section)

        # Filtrar por fabricante
        factory = self.request.GET.get('factory')
        if factory:
            queryset = queryset.filter(factory__icontains=factory)

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductType.objects.all()
        context['departments'] = Product.objects.values_list(
            'department', flat=True).distinct().order_by('department')
        context['sections'] = Product.objects.values_list(
            'section', flat=True).distinct().order_by('section')
        context['factories'] = Product.objects.values_list(
            'factory', flat=True).distinct().order_by('factory')
        return context


def cart_view(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(
            user=request.user, status='pending')
    else:
        order, created = Order.objects.get_or_create(
            user=None, status='pending')
    cart_items = OrderProduct.objects.filter(order_id=order) if order else []
    cart_total = sum(item.unity_price *
                     item.quantity for item in cart_items) if order else 0
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(request, 'cart.html', context)


def update_cart(request):
    product_id = request.GET.get('product_id')
    quantity = int(request.GET.get('quantity', 1))
    product = Product.objects.get(id=product_id)
    total = 0
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(
            user=request.user, status='pending')
    else:
        order, created = Order.objects.get_or_create(
            user=None, status='pending')
    order_product, created = OrderProduct.objects.get_or_create(order_id=order, product_id=product,
                                                                defaults={'quantity': quantity, 'unity_price': product.price, })
    order_product.quantity = quantity
    order_product.unity_price = product.price
    orderProducts = OrderProduct.objects.filter(order_id=order)
    for orderProduct in orderProducts:
        total += orderProduct.unity_price * orderProduct.quantity
    if total >= 20:
        order.shipping_price = 0.00
    else:
        order.shipping_price = 5.00
    print(order.shipping_price)
    order.save()
    order_product.save()
    return redirect('cart')


def remove_from_cart(request):
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
    total = 0.00
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(
            user=request.user, status='pending')
    else:
        order, created = Order.objects.get_or_create(
            user=None, status='pending')
    order_product, created = OrderProduct.objects.get_or_create(
        order_id=order, product_id=product)
    orderProducts = OrderProduct.objects.filter(order_id=order)
    for orderProduct in orderProducts:
        total += orderProduct.unity_price * orderProduct.quantity
    if total >= 20:
        order.shipping_price = 0.00
    else:
        order.shipping_price = 5.00
    order.save()
    order_product.delete()
    return redirect('cart')


def order_confirmation_view(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(
            user=request.user, status='pending')
        email = request.user.email
    else:
        order, created = Order.objects.get_or_create(
            user=None, status='pending')
        email = ""
    cart_items = OrderProduct.objects.filter(order_id=order) if order else []
    cart_total = sum(item.unity_price *
                     item.quantity for item in cart_items) if order else 0
    if cart_total >= 20:
        order.shipping_price = 0.00
    else:
        order.shipping_price = 5.00
    order.save()

    context = {
        'email': email,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'authenticated': request.user.is_authenticated,
        'order': order,
    }
    return render(request, 'order_confirmation.html', context)


def confirmed_order(request):
    email = request.POST.get('email')
    payment_method = request.POST.get('payment_method')
    country = request.POST.get('country')
    city = request.POST.get('city')
    postal_code = request.POST.get('postal_code')
    street = request.POST.get('street')
    number = int(request.POST.get('number'))
    apartment_number = request.POST.get('apartment_number', None)
    address, created = Address.objects.get_or_create(
        country=country, city=city, postal_code=postal_code, street=street, number=number, apartment_number=apartment_number)
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(
            user=request.user, status='pending')
        address.user = request.user
        address.save()
        first_name = request.user.first_name
        last_name = request.user.last_name
    else:
        order, created = Order.objects.get_or_create(
            user=None, status='pending')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

    order.address = address
    request.session['first_name'] = first_name
    request.session['last_name'] = last_name
    subject = "Pedido realizado con éxito"
    message = f"""
    Estimado {first_name} {last_name},

    ¡Gracias por tu compra en RitualUS! Tu pedido ha sido confirmado.

    Detalles del Pedido:
    Número de Pedido: {order.id}
    Dirección de Entrega: {address.street} {address.number}, {address.city}, {address.country}, Código Postal: {address.postal_code}

    Método de pago: {payment_method}
    """

    for order_product in order.order_product.all():
        product = order_product.product_id
        message += f"- {product.name}: {order_product.quantity} x {product.price}€\n"

    total_price = sum(
        product.quantity * product.unity_price for product in order.order_product.all())
    message += f"\nTotal: {total_price}€"

    send_mail(subject=subject, message=message,
              from_email="ritualus@gmail.com", recipient_list=[email])
    if payment_method == 'cash':
        order.payment = 'cash'
        order.status = 'in delivery'
    elif payment_method == 'card':
        order.payment = 'credit card'
        order.status = 'confirmed'
        order.save()
        return redirect('payment', order_id=order.id)
    order.save()
    return redirect(f'/payment/success/{order.id}/')


class ProductDetailView(DetailView):
    template_name = 'product_detail.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        recommended_products = Product.objects.filter(
            product_type=product.product_type).exclude(id=product.id)[:9]
        context['recommended_products'] = recommended_products
        return context


class CartView(View):
    def get(self, request):
        # Mostrar el carrito
        cart_items = request.session.get('cart_items', [])
        return render(request, 'cart.html', {'cart_items': cart_items})

    def post(self, request):
        # Crear una lista de productos de prueba para el carrito
        cart_items = [
            {'product_id': 1, 'name': 'Producto 1', 'price': 1, 'quantity': 1},
            {'product_id': 2, 'name': 'Producto 2', 'price': 2, 'quantity': 1},
            {'product_id': 3, 'name': 'Producto 3', 'price': 3, 'quantity': 1},
        ]
        # Guardar los productos en la sesión
        request.session['cart_items'] = cart_items

        # Redirigir al usuario a la página de pago
        return redirect('payment')


class PaymentSuccessView(View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        order_products = OrderProduct.objects.filter(order_id=order_id)
        address = order.address
        user = request.user
        order.status = 'in delivery'
        order.save()
        total_price = 0
        for product in order_products:
            if product.product_id.discount_price:
                total_price += product.product_id.discount_price * product.quantity
            else:
                total_price += product.product_id.price * product.quantity

        if user.is_authenticated:
            first_name = user.first_name
            last_name = user.last_name
        else:
            first_name = request.session.get('first_name', 'Desconocido')
            last_name = request.session.get('last_name', 'Desconocido')

        return render(request, 'payment_success.html', {'total_price': total_price, 'address': address, 'order_id': order_id, 'order': order, 'order_products': order_products, 'first_name': first_name, 'last_name': last_name})


class PaymentView(View):
    def get(self, request, order_id):
        order_products = OrderProduct.objects.filter(order_id=order_id)
        order = Order.objects.get(id=order_id)
        address = order.address
        products = []
        total_price = 0

        for item in order_products:
            product = item.product_id
            if product.discount_price:
                total_price += product.discount_price * item.quantity
            else:
                total_price += product.price * item.quantity

            products.append({
                'name': product.name,
                'price': product.price,
                'discount_price': product.discount_price,
                'quantity': item.quantity,
                'address': address,
            })

        payment_intent = stripe.PaymentIntent.create(
            amount=int(total_price * 100),
            currency='eur',
            description='Pago de productos'
        )
        print(order.shipping_price)
        return render(request, 'payment.html', {
            'order_products': order_products,
            'total_price': total_price,
            'client_secret': payment_intent.client_secret,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLISHABLE_KEY,
            'order_id': order_id,
            'order': order,
        })

    def post(self, request):
        order = Order.objects.get(id=order_id)
        cart_items = request.session.get('products', [])

        total_amount = 0
        line_items = []
        for item in cart_items:
            product = Product.objects.get(id=item['product_id'])
            total_amount += product.price * item['quantity']
            line_items.append({
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': product.name,
                    },
                    'unit_amount': product.price * 100,
                },
                'quantity': item['quantity'],
            })

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url='http://localhost:8000/success',
                cancel_url='http://localhost:8000/cancel',
            )
            return JsonResponse({
                'id': checkout_session.id
            })
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=500)


def contact(request):
    if request.method == 'POST':
        # Se capturan los datos del formulario
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Se prepara el correo para la empresa
        subject_to_company = f"Nuevo mensaje de contacto de {name}"
        message_to_company = f"Nombre: {
            name}\nEmail: {email}\nMensaje:\n{message}"
        recipient_list_company = ['ritualusinfo@gmail.com']

        # Se prepara el correo de confirmación para el usuario
        subject_to_user = "Confirmación de tu mensaje en RitualUS"
        message_to_user = f"Hola {name},\n\nGracias por contactarnos. Hemos recibido tu mensaje:\n\n{
            message}\n\nNos pondremos en contacto contigo pronto.\n\nSaludos,\nRitualUS"
        recipient_list_user = [email]

        try:
            # Se envían los correos (aparecerá en la consola)
            send_mail(subject_to_company, message_to_company,
                      'ritualusinfo@gmail.com', recipient_list_company)
            send_mail(subject_to_user, message_to_user,
                      'ritualusinfo@gmail.com', recipient_list_user)
            # Si tiene éxito:
            messages.success(
                request, '¡Tu mensaje ha sido enviado exitosamente! Revisa la consola para simular el envío de correos.')
        except Exception as e:
            # Si ocurre un error:
            messages.error(
                request, f'Ocurrió un error al enviar tu mensaje: {e}')

        # Se redirige de nuevo a la página de contacto
        return redirect('contact')
    # Si no es POST, simplemente renderiza la plantilla
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')


def order_tracking_view(request):
    order = None
    order_products = None
    if request.GET.get('order_id'):
        order_id = request.GET['order_id']
        try:
            order = Order.objects.get(id=order_id, user_id=request.user.id)
            order_products = OrderProduct.objects.filter(order_id=order)
            time_to_delivered = now() - order.date
            if time_to_delivered >= timedelta(minutes=5):
                order.status = 'delivered'
                order.save()
        except Order.DoesNotExist:
            order = None
            order_products = None
    return render(request, 'order_tracking.html', {'order': order, 'order_products': order_products})


def search_products(request):
    query = request.GET.get('query', '')
    print(query)
    if query:
        
        products = Product.objects.filter(name__icontains=query)[:10]  
        print(products)
        results = [{'id': product.id, 'name': product.name} for product in products]
        print(results)
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})
