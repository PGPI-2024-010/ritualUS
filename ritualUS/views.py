
from django.views.generic import ListView, DetailView
from .models import Product, Category
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
        

class ProductDetailView(DetailView):
    template_name = 'product_detail.html' 
    model = Product 
    context_object_name = 'product'