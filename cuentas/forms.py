from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UsernameForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder':'Nombre de usuario'}))

class PasswordForm(forms.Form):
    username = forms.CharField(widget=forms.HiddenInput())
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Contraseña'}))

class ForgotUsernameForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Correo electrónico'}))

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese su apellido'})
    )
    username = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'})
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'})
    )
    
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'placeholder':'Contraseña'}))
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'placeholder':'Confirmar contraseña'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("Ya existe un usuario con ese correo.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

from django import forms
from informe.models import Informe
import datetime



class InformeForm(forms.ModelForm):
    class Meta:
        model = Informe
        fields = [ "año","mes", "participacion", "estudios", "auxiliar", "horas", "notas"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            # Estilo base de todos los campos
            css_class = "form-control"

            # Ajuste si es booleano (ej. auxiliar como checkbox)
            if isinstance(field.widget, forms.CheckboxInput):
                css_class = "form-check-input"

            # Ajuste si es textarea (ej. notas)
            if isinstance(field.widget, forms.Textarea):
                css_class = "form-control"  # ya está bien, pero por claridad

            field.widget.attrs.update({
                "class": css_class,
            })

