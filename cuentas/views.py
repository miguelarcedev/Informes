
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from collections import defaultdict
from publicador.models import Publicador
from informe.models import Informe
from .forms import UsernameForm, PasswordForm, RegisterForm, ForgotUsernameForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import InformeForm
from django.db import IntegrityError, transaction
from django.contrib.auth.decorators import user_passes_test

def login_username(request):
    if request.user.is_authenticated:
        return redirect('mi_panel')
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
        return redirect('mi_panel')
    username = request.session.get('tmp_username')
    if not username:
        return redirect('login_username')
    form = PasswordForm(request.POST or None, initial={'username': username})
    if request.method == 'POST' and form.is_valid():
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('mi_panel')
        else:
            form.add_error('password', 'Contraseña incorrecta.')
    return render(request, 'cuentas/login_password.html', {'form': form, 'username': username})

def register(request):
    if request.user.is_authenticated:
        return redirect('mi_panel')
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
def mi_panel(request):
    publicador = None
    informes = None

    try:
        # Asumiendo que en Publicador hay un campo OneToOne con User
        publicador = request.user.publicador
        #publicador = getattr(request.user, 'publicador', None)
        informes = Informe.objects.filter(publicador=publicador)
    except Publicador.DoesNotExist:
        publicador = None


    informes_agrupados = defaultdict(list)
    if informes:
        for informe in informes:
            # Agrupa los informes por el año
            informes_agrupados[informe.año].append(informe)
    
    # Ordena los años de forma descendente
    años_ordenados = sorted(informes_agrupados.keys(), reverse=True)  
    form_inicial = InformeForm()
   
    context = {
        # ... otros datos del contexto ...
        'publicador': publicador,
        'informes_agrupados': informes_agrupados,
        'años_ordenados': años_ordenados,
        'form_inicial': form_inicial
    }
    return render(request, 'cuentas/mi_panel.html', context)

  

def do_logout(request):
    logout(request)
    messages.info(request, "Has cerrado sesión.")
    return redirect('login_username')


@login_required
def crear_informe(request):
    publicador = request.user.publicador

    if request.method == "POST":
        form = InformeForm(request.POST)
        if form.is_valid():
            informe = form.save(commit=False)
            informe.publicador = publicador
            try:
                with transaction.atomic():
                    informe.save()
                messages.success(request, "✅ Informe creado correctamente.")
                return redirect("mi_panel")  # 👈 redirige a la vista que muestra los tabs
            except IntegrityError:
                form.add_error(None, "Ya existe un informe para ese mes y año.")
    else:
        form = InformeForm()

    return render(request, "informes/crear_informe.html", {"form": form})


@login_required
def editar_informe(request, pk):
    publicador = request.user.publicador
    informe = get_object_or_404(Informe, pk=pk, publicador=publicador)

    if request.method == "POST":
        form = InformeForm(request.POST, instance=informe)
        if form.is_valid():
            form.save()
            return redirect('mi_panel')
    else:
        form = InformeForm(instance=informe)

    return render(request, 'informes/editar_informe.html', {'form': form})


# Solo permite acceso si el usuario es staff
@user_passes_test(lambda u: u.is_staff)
def panel_general(request):
    return render(request, "panel_general.html")
