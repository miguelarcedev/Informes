from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime
from informe.models import Informe

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


 
# forms.py
import datetime
from django import forms

class InformeForm(forms.ModelForm):
    class Meta:
        model = Informe
        fields = ["año", "mes", "participacion", "estudios", "servicio", "horas", "notas"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ======= LÓGICA DE AÑO Y MES AUTOMÁTICO =======
        hoy = datetime.date.today()
        dia, mes, anio = hoy.day, hoy.month, hoy.year

        # Si es antes del 25 → usar mes anterior
        if dia < 25:
            mes -= 1
            if mes == 0:  # caso enero → diciembre del año anterior
                mes = 12
                anio -= 1

        # Determinar año académico
        if mes >= 10:  # octubre a diciembre → año académico siguiente
            anio_academico = anio + 1
        else:  # enero a septiembre → año académico actual
            anio_academico = anio

        # Preasignar valores iniciales
        self.fields["año"].initial = anio_academico
        self.fields["mes"].initial = mes  # ✅ número (coincide con el modelo)

        # ======= ESTILOS =======
        for field_name, field in self.fields.items():
            css_class = "form-control"
            if isinstance(field.widget, forms.CheckboxInput):
                css_class = "form-check-input"
            if isinstance(field.widget, forms.Textarea):
                css_class = "form-control"
            field.widget.attrs.update({"class": css_class})

    def clean(self):
        cleaned_data = super().clean()
        año = cleaned_data.get("año")
        mes = cleaned_data.get("mes")
        publicador = getattr(self.instance, "publicador", None)  # viene de la instancia

        if publicador and año and mes:
            # Buscar otro informe con mismo publicador/año/mes
            existe = Informe.objects.filter(
                publicador=publicador,
                año=año,
                mes=mes
            ).exclude(pk=self.instance.pk).exists()

            if existe:
                msg = "Ya existe un informe para este publicador en ese año y mes."
                self.add_error("año", msg)
                self.add_error("mes", msg)

        return cleaned_data
