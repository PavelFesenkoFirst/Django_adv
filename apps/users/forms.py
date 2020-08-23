from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'email', 'phone', 'name', 'password1', 'password2', 'location'
        )
