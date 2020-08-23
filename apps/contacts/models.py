from django.db import models
from django.conf import settings
from django.core.mail import send_mass_mail

# Create your models here.


class Contacts(models.Model):
    title = models.CharField(max_length=128)
    address = models.TextField()
    phone = models.CharField(max_length=20)



    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'title': 'advertising board',
                'address': 'Kharkiv, some street',
                'phone': '0661122333'
            }
        )
        return obj


class ContactUs(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'contact us'

    def __str__(self):
        return self.name


    messages = (
        ('Новое сообщение', f'На сайте зарегистрированно новая "форма связи", проверьте его',
         settings.EMAIL_HOST_USER, ['truemewmoonkloom@gmail.com']),
        ('Новое сообщение', f'На сайте зарегистрированно новая "форма связи", проверьте его',
         settings.EMAIL_HOST_USER, ['pavelfesenko.work@gmail.com']),
    )

    def email_send(self):
        send_mass_mail(self.messages)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)