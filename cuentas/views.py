from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

from .forms import UsernameForm, PasswordForm, RegisterForm, ForgotUsernameForm
from django.contrib.auth.models import User

def login_username(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = UsernameForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            request.session['tmp_username'] = username
            return redirect('login_password')
        else:
            form.add_error('username', 'Este usuario no existe.')
    return render(request, 'cuentas/login_username.html', {'form': form})

def login_password(request):
    if request.user.is_authenticated:
        return redirect('home')
    username = request.session.get('tmp_username')
    if not username:
        return redirect('login_username')
    form = PasswordForm(request.POST or None, initial={'username': username})
    if request.method == 'POST' and form.is_valid():
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            form.add_error('password', 'Contraseña incorrecta.')
    return render(request, 'cuentas/login_password.html', {'form': form, 'username': username})

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Cuenta creada. Ahora puedes iniciar sesión.")
        return redirect('login_username')
    return render(request, 'cuentas/register.html', {'form': form})

def forgot_username(request):
    form = ForgotUsernameForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        users = User.objects.filter(email=email)
        if users.exists():
            subject = render_to_string('emails/forgot_username_subject.txt').strip()
            body = render_to_string('emails/forgot_username_email.txt', {'users': users})
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or settings.EMAIL_HOST_USER
            send_mail(subject, body, from_email, [email])
            messages.success(request, "Te enviamos tu(s) usuario(s) al correo.")
            return redirect('login_username')
        else:
            form.add_error('email', 'No hay cuentas vinculadas a ese correo.')
    return render(request, 'cuentas/forgot_username.html', {'form': form})

@login_required
def home(request):
    return render(request, 'cuentas/home.html')

def do_logout(request):
    logout(request)
    messages.info(request, "Has cerrado sesión.")
    return redirect('login_username')
