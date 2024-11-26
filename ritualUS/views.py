
from django.views.generic import ListView, DetailView
from .models import Product, Category, Order, OrderProduct
from django.contrib.auth.decorators import login_required
from .forms import CustomSignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages

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
            return redirect('account_login')  # Redirige al login o a la página que prefieras
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

def cart_view(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, status='pending')
    else:
        order, created = Order.objects.get_or_create(status='pending')
    cart_items = OrderProduct.objects.filter(order_id=order) if order else []
    cart_total = sum(item.unity_price * item.quantity for item in cart_items) if order else 0
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(request, 'cart.html', context)

def update_cart(request):
    product_id = request.GET.get('product_id')
    quantity = int(request.GET.get('quantity', 1))
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, status='pending')
    else:
        order, created = Order.objects.get_or_create(status='pending')
    order_product, created = OrderProduct.objects.get_or_create(order_id=order, product_id=product,
                                                                defaults={'quantity':quantity,'unity_price':product.price,})
    order_product.quantity = quantity
    order_product.unity_price = product.price
    order_product.save()
    return redirect('cart')

def remove_from_cart(request):
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, status='pending')
    else:
        order, created = Order.objects.get_or_create(status='pending')
    order_product, created = OrderProduct.objects.get_or_create(order_id=order, product_id=product)
    order_product.delete()
    return redirect('cart')

class ProductDetailView(DetailView):
    template_name = 'product_detail.html' 
    model = Product 
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        recommended_products = Product.objects.filter(product_type=product.product_type).exclude(id=product.id)[:9]
        context['recommended_products'] = recommended_products
        return context
    
def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')
