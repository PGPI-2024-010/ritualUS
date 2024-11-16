
from django.views.generic import ListView
from .models import Item, Category
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render

class Home(ListView):
    template_name = 'index.html'
    queryset = Item.objects.filter(is_active=True)
    context_object_name = 'items'


