
from django.views.generic import ListView
from .models import Product, Category
from django.contrib.auth.decorators import login_required
from .forms import CustomSignupForm
from django.shortcuts import render


class Home(ListView):
    template_name = 'index.html'
    queryset = Product.objects.filter(is_available=True)
    context_object_name = 'items'

    

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})