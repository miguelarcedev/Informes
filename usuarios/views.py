# usuarios/views.py
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .forms import RegistroForm

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.is_active = False  # usuario inactivo hasta confirmación
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()

            # Enviar email de activación
            current_site = get_current_site(request)
            subject = 'Activa tu cuenta'
            message = render_to_string('activar_email.html', {
                'usuario': usuario,
                'dominio': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(usuario.pk)),
                'token': default_token_generator.make_token(usuario),
            })
            send_mail(subject, message, None, [usuario.email])
            messages.success(request, 'Revisa tu correo para activar tu cuenta.')
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def activar(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        usuario = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        usuario = None

    if usuario and default_token_generator.check_token(usuario, token):
        usuario.is_active = True
        usuario.save()
        messages.success(request, '¡Cuenta activada! Ya puedes iniciar sesión.')
        return redirect('home')
    else:
        messages.error(request, 'El enlace de activación no es válido o ha expirado.')
        return redirect('registro')

