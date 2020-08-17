from django.contrib import admin

from .models import Contacts, ContactUs
# Register your models here.


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    pass

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    pass