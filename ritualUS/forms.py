from django import forms
from allauth.account.forms import SignupForm
from allauth.account.forms import LoginForm

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=100, label="Nombre")
    last_name = forms.CharField(max_length=100, label="Apellidos")
    phone_number = forms.CharField(max_length=15, label="Número de Teléfono")
    dni = forms.CharField(max_length=20, label="DNI")
    
    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.dni = self.cleaned_data['dni']
        user.save()
        return user
