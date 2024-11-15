from django import forms
from allauth.account.forms import SignupForm
from .models import CustomUser

class CustomSignupForm(SignupForm):
    name = forms.CharField(max_length=30, required=True)
    surname = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=15, required=True)
    DNI = forms.CharField(max_length=9, required=True)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['Name:']
        user.last_name = self.cleaned_data['Surname:']
        user.phone_number = self.cleaned_data['Phone:']
        user.dni = self.cleaned_data['DNI:']
        user.save()
        return user