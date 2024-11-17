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
        user.profile.phone_number = self.cleaned_data['phone_number']
        user.profile.dni = self.cleaned_data['dni']
        user.save()
        return user
    
class CustomLoginForm(LoginForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añadir atributos personalizados si deseas estilizar el formulario
        self.fields['login'].widget.attrs['placeholder'] = 'Correo o Nombre de usuario'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'