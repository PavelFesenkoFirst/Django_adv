from django.db import models

# Create your models here.

class CityLocation(models.Model):

    LOCATIONS = (
        ('Киев', 'Киев'),
        ('Харьков', 'Харьков'),
        ('Одесса', 'Одесса'),
        ('Донецк', 'Донецк'),
        ('Запорожье', 'Запорожье'),
        ('Днепр', 'Днепр'),
        ('Ивано', 'Ивано-Франковск'),
        ('Чернигов', 'Чернигов'),
        ('Херсон', 'Херсон'),
        ('Житомир', 'Житомир'),
        ('Хмельницк', 'Хмельницк'),
        ('Ужгород', 'Ужгород'),
        ('Львов', 'Львов'),
        ('Луцк', 'Луцк'),
        ('Черновцы', 'Черновцы'),

    )

    location = models.CharField(max_length=50, verbose_name='города', choices=LOCATIONS)

    def __str__(self):
        return self.location