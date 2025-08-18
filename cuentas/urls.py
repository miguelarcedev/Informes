from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #path('login/username/', views.login_username, name='login_username'),
    path('', views.login_username, name='login_username'),
    path('login/password/', views.login_password, name='login_password'),
    path('register/', views.register, name='register'),
    path('forgot-username/', views.forgot_username, name='forgot_username'),
    path('logout/', views.do_logout, name='logout'),
    path('home/', views.home, name='home'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='cuentas/password_reset_form.html',
        email_template_name='emails/password_reset_email.txt',
        subject_template_name='emails/password_reset_subject.txt',
        success_url='/password-reset/done/'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='cuentas/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='cuentas/password_reset_confirm.html',
        success_url='/password-reset-complete/'
    ), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='cuentas/password_reset_complete.html'
    ), name='password_reset_complete'),

    path('informes/nuevo/', views.crear_informe, name='crear_informe'),
    path('informes/<int:pk>/editar/', views.editar_informe, name='editar_informe'),
    path("staff/", views.panel_staff, name="pagina_staff"),
]
