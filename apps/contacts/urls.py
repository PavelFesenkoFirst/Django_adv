from django.urls import path

from apps.contacts.views import contact_us


app_name = 'core'

urlpatterns = [
    path('contact_us/', contact_us, name='contact-us'),
]
