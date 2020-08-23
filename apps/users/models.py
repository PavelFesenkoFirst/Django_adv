from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

from .managers import CustomUserManager
from apps.location.models import CityLocation

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    location = models.ForeignKey(CityLocation, on_delete=models.CASCADE, null=True, related_name='city')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'custom user'
        verbose_name_plural = 'custom users'

    def email_user(self, subject, message, **kwargs):
        send_mail(
            subject, message, settings.EMAIL_HOST_USER, [self.email], **kwargs
        )

    def get_absolute_url(self):
        return reverse('users:profile')


    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)