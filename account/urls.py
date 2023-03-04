from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import (UserLoginForm)

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
    path('logout/', auth_views.LogoutView.as_view(next_page = '/account/login/'), name = 'logout')
]