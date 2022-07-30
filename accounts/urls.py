from django.contrib.auth.views import *
from django.urls import path
from django.views.generic import TemplateView

from . import views
from .forms import PasswordResetForm, PwdResetConfirm, UserLoginForm

app_name= 'accounts'

urlpatterns = [
    # Login and Register View
    path('register/',views.register,name='register'),
    path('activate/<slug:uidb64>/<slug:token>/',views.activate,name='activate'),
    path('login/',LoginView.as_view(form_class=UserLoginForm,template_name='accounts/login.html'),name='login'),
    path('logout/',LogoutView.as_view(next_page='/accounts/login/'),name='logout'),
    #Password Reset

    path('password-reset/',PasswordResetView.as_view(form_class=PasswordResetForm,template_name='accounts/password_reset_form.html',email_template_name='accounts/password_reset_email.html',success_url = 'password-reset-email-confirm/'),name='pwdreset'),
    path('password-reset/password-reset-email-confirm/',TemplateView.as_view(template_name='accounts/reset_status.html'),name='password_reset_email_confirm'),
    path('password-reset-confirm/<slug:uidb64>/<slug:token>/',PasswordResetConfirmView.as_view(form_class=PwdResetConfirm,template_name='accounts/password_reset_confirm.html',success_url = 'password_reset_complete/'),name='password_reset_confirm'),
    path('password_reset_complete/',TemplateView.as_view(template_name = 'password_reset_complete.html'),name='password_reset_complete'),
    path('password_reset_confirm/Mg/password_reset_complete',TemplateView.as_view(template_name='account/user/reset_status.html'),name='password_reset_complete'),


    # Create and Edit Poll
    path('create-poll/',views.create_poll, name='create_poll'),
    path('add-choices',views.create_option,name='add_choices'),
    path('edit-poll/',views.edit_poll,name='edit_poll'),
    path('vote/',views.vote,name='vote')
    
]
