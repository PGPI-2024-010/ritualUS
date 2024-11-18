
from django.views.generic import ListView
from .models import Product, Category
from django.contrib.auth.decorators import login_required
from .forms import CustomSignupForm
from django.shortcuts import render, redirect


class Home(ListView):
    template_name = 'index.html'
    queryset = Product.objects.filter(is_available=True)
    context_object_name = 'items'

    
def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo usuario
            return redirect('account_login')  # Redirige al login o a la página que prefieras
    else:
        form = CustomSignupForm()
    
    return render(request, 'signup.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})