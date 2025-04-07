from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('questions.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),   
] 