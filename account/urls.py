from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from .forms import (UserLoginForm, PWRestConfirmForm, PWRestForm)
from . import views


app_name = 'account'
urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate_user, name='activate'),
    path('dashboard/',views.user_dashboard, name='dashboard'),
    
    # auth views
    path('login/', auth_views.LoginView.as_view(
        template_name = 'account/login.html',
        form_class = UserLoginForm,
        
    ), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(next_page = '/account/login/'), name = 'logout'),
    path('edit/', views.profile_edit, name = 'profile-edit'),
    path('delete_user/', views.delete_user, name='delete-user'),
    path('delete-confirm/', TemplateView.as_view(
        template_name= 'account/user/delete_confirm.html'
        ), name='delete-confirmation'),
    path('password-rest/', auth_views.PasswordResetView.as_view(
        template_name = 'account/user/password_reset_form.html',
        success_url = 'password-reset-email-confirm',
        email_template_name = 'account/components/password_reset_email.html',
        form_class = PWRestForm
        ), name='pwdreset'),
    
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(
             template_name = 'account/user/password_reset_confirm.html',
             success_url = '/account/password-reset-complete/',
             form_class = PWRestConfirmForm
             ),
         name='password_reset_confirm'),
    path('password-rest/password-reset-email-confirm/', TemplateView.as_view(
        template_name = 'account/user/reset_status.html'
    ), name = 'password_reset_done'),
    path('password-reset-complete/', 
         TemplateView.as_view(
             template_name = 'account/user/reset_status.html'
        ),  name = 'password_reset_complete')
    
    
]