from django.db import models

# Create your models here.


class Contacts(models.Model):
    title = models.CharField(max_length=128)
    address = models.TextField()
    phone = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

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
