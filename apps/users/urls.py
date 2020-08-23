from django.urls import path
from .views import (RegisterView, ProfileView, LogoutView, LoginView, ChangeName, ChangeCity)

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('edit_name/<int:pk>/edit', ChangeName.as_view(), name='edit_name'),
    path('edit_city/<int:pk>/edit/', ChangeCity.as_view(), name='edit_city'),

]