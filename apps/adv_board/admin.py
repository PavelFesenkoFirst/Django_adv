from django.contrib import admin


from .models import Rubric, Category, Advertisement, FavoriteAd

@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('rubric_id', 'name',)


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'id_category', 'id_user', 'date_creation', 'date_upd', 'in_active', 'in_moderation',
                    'is_locked')

@admin.register(FavoriteAd)
class FavoriteAdAdmin(admin.ModelAdmin):
    list_display = ('id_adv', 'id_user',)