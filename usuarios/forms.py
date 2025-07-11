# usuarios/forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirmacion = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Confirmar contraseña")

    class Meta:
        model = User
        fields = ['last_name', 'first_name','username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("password_confirmacion"):
            raise ValidationError("Las contraseñas no coinciden")
        return cleaned_data
