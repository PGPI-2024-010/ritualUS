from django import forms
from allauth.account.forms import SignupForm
from allauth.account.forms import LoginForm

from ritualUS.models import CustomUser

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=100, label="Nombre")
    last_name = forms.CharField(max_length=100, label="Apellidos")
    phone_number = forms.CharField(max_length=15, label="Número de Teléfono")
    dni = forms.CharField(max_length=20, label="DNI")
    
    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if CustomUser.objects.filter(dni=dni).exists():
            raise forms.ValidationError("El DNI ya está registrado. Por favor, usa otro.")
        return dni

    def save(self, request):
        user = super().save(request)  # El super ya guarda el usuario en la base de datos
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.dni = self.cleaned_data['dni']
        user.save(update_fields=['first_name', 'last_name', 'phone_number', 'dni'])  # Solo actualiza campos    
        return user
