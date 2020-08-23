from django.contrib import admin

from apps.location.models import CityLocation

# Register your models here.

@admin.register(CityLocation)
class RubricAdmin(admin.ModelAdmin):
    list_display = ('location',)