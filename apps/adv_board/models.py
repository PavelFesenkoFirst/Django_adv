from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from apps.users.models import CustomUser


# Create your models here.

class Rubric(models.Model):
    name = models.CharField(max_length=128, verbose_name='название рубрики')
    slug = models.SlugField(allow_unicode=True, default='', blank=True,)

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ('-name',)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('adv_board:rubric-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Category(models.Model):
    rubric_id = models.ForeignKey(Rubric, on_delete=models.CASCADE, null=True, related_name='rubric')
    name = models.CharField(max_length=128, verbose_name='категория')
    slug = models.SlugField(allow_unicode=True, default='', blank=True,)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('-name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('adv_board:category-detail', kwargs={
            'slug_rubric': self.rubric_id.slug,
            'pk': self.pk
        })
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Advertisement(models.Model):
    title = models.CharField(max_length=128, verbose_name='заголовок')
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='adv_category')
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(verbose_name='изображение', upload_to='advertisement', blank=True, null=True,)
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='adv_user')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    date_upd = models.DateTimeField(auto_now=True, verbose_name='дата изменения')
    in_active = models.BooleanField(default=False, verbose_name='статус')
    in_moderation = models.BooleanField(default=True, verbose_name='проверка')
    is_locked = models.BooleanField(default=False, verbose_name='заблокировано')
    count_view = models.IntegerField(default=0, verbose_name='просмотры')
    status_vip = models.BooleanField(default=False, verbose_name='vip')
    price = models.IntegerField(verbose_name='цена')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def get_absolute_url(self):
        return reverse('adv_board:adv-detail', kwargs={
            'slug_category': self.id_category.slug,
            'pk': self.pk
        })

    def __str__(self):
        return self.title


class FavoriteAd(models.Model):
    id_adv = models.ForeignKey(Advertisement, on_delete=models.CASCADE, null=True, related_name='favorite_adv')
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='favorite_user')

    def __str__(self):
        return self.id_adv.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Feedback(models.Model):
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='feedback_user')
    topic = models.ForeignKey(Advertisement, on_delete=models.CASCADE, null=True, related_name='feedback_adv')
    message = models.TextField(verbose_name='сообщение')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
