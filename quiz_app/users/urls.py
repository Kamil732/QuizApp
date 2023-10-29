from django.urls import path, include
from django.contrib.auth.decorators import login_required

from .decorators import unautthenticated_user
from . import views

app_name = 'users'
urlpatterns = [
    path('login', unautthenticated_user(views.LoginView.as_view()), name='login'),
    path('register', unautthenticated_user(views.RegisterView.as_view()), name='register'),
    path('logout', views.LoginView.as_view(), name='logout'),
    path('profile-settings', login_required(views.ProfileSettingsView.as_view(), login_url='users:login'), name='profile-settings'),
    path('profile/<slug:slug>/<int:page>', login_required(views.ProfileView.as_view(), login_url='users:login'), name='profile'),
]