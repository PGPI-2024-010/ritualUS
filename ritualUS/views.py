
from django.views.generic import ListView, DetailView
from .models import Product, Category, OrderProduct, Order
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
load_dotenv()
stripe.api_key = os.getenv('STRIPE_API_KEY')


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
        category_id = self.request.GET.get('category')
        if category_id:
            # Filtra los productos por la categoría seleccionada
            return Product.objects.filter(product_type_id=category_id)
        else:
            # Si no hay filtro, muestra todos los productos
            return Product.objects.all()


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
        total_price = 0
        for product in order_products:
            if product.product_id.discount_price:
                total_price += product.product_id.discount_price * product.quantity
            else:
                total_price += product.product_id.price * product.quantity
        return render(request, 'payment_success.html', {'total_price': total_price, 'address': address, 'order_id': order_id, 'order': order, 'order_products': order_products, 'user': user})


class PaymentView(View):
    def get(self, request, order_id):
        # Obtener los productos asociados al pedido
        order_products = OrderProduct.objects.filter(order_id=order_id)
        address = Order.objects.get(id=order_id).address
        # Inicializar una lista para los productos con su información
        products = []
        total_price = 0

        for item in order_products:
            product = item.product_id  # Acceder al producto relacionado con OrderProduct
            if product.discount_price:
                # Calcular el precio total con descuento
                total_price += product.discount_price * item.quantity
            else:
                total_price += product.price * item.quantity  # Calcular el precio total

            # Añadir el producto a la lista
            products.append({
                'name': product.name,
                'price': product.price,
                'discount_price': product.discount_price,  # Si tiene descuento
                'quantity': item.quantity,
                'address': address,
            })

        # Crear un PaymentIntent de Stripe
        payment_intent = stripe.PaymentIntent.create(
            amount=int(total_price * 100),  # Convertir a centavos
            currency='eur',
            description='Pago de productos'
        )

        return render(request, 'payment.html', {
            'order_products': order_products,  # Pasa los productos con los detalles
            'total_price': total_price,
            'client_secret': payment_intent.client_secret,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLISHABLE_KEY,
            'order_id': order_id,
        })

    def post(self, request):
        cart_items = request.session.get('products', [])

        total_amount = 0
        line_items = []
        for item in cart_items:
            # Obtener el producto de la base de datos
            product = Product.objects.get(id=item['product_id'])
            # Calcular el precio total por producto
            total_amount += product.price * item['quantity']
            line_items.append({
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': product.name,  # Nombre del producto
                    },
                    # Precio en centavos (Stripe usa centavos)
                    'unit_amount': product.price * 100,
                },
                # Cantidad de este producto en el carrito
                'quantity': item['quantity'],
            })

        try:
            # Crear la sesión de pago de Stripe con el total calculado
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],  # Aceptar pagos con tarjeta
                line_items=line_items,  # Los productos que el usuario va a pagar
                mode='payment',  # Modo de pago único
                success_url='http://localhost:8000/success',  # URL de éxito
                cancel_url='http://localhost:8000/cancel',    # URL de cancelación
            )
            return JsonResponse({
                'id': checkout_session.id  # Regresar el ID de la sesión para redirigir al frontend
            })
        except Exception as e:
            return JsonResponse({
                'error': str(e)  # Devolver el error si ocurre algún problema
            }, status=500)
