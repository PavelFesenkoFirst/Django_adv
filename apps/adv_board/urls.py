from django.urls import path
from .views import (IndexTemplateView, rubric_detail, RubricListView, CategoryListView, category_detail,
                    SearchView, adv_detail, adv_create, AdvEdit, AdvertisementListView,
                    moderation_list, HiddenAdvView, LockedAdvUserView, FavoriteTemplateView, PublicationAdvView,
                    FavouriteAdvView)

app_name = 'adv_board'

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('rubric/', RubricListView.as_view(), name='rubric-list'),
    path('rubric/<slug>', rubric_detail, name='rubric-detail'),
    path('category/', CategoryListView.as_view(), name='category-list'),
    path('category/<slug_rubric>/<pk>', category_detail, name='category-detail'),
    path('advertisement/', AdvertisementListView.as_view(), name='adv-list'),
    path('advertisement/<slug_category>/<pk>', adv_detail, name='adv-detail'),
    path('create_adv/', adv_create, name='create_adv'),
    path('adv_edit/<int:pk>/edit', AdvEdit.as_view(), name='adv_edit'),
    path('search/', SearchView.as_view(), name='search'),
    path('favorite/<pk>', FavoriteTemplateView.as_view(), name='favorite-adv'),
    path('adv_moderation/', moderation_list, name='moderation-list'),
    path('hidden/<pk>/', HiddenAdvView.as_view(), name='hidden-adv'),
    path('locked/<pk>/', LockedAdvUserView.as_view(), name='locked-adv'),
    path('publication/<pk>/', PublicationAdvView.as_view(), name='publication-adv'),
    # path('add/<pk>/', FavoriteAddView.as_view(), name='favourite-add'),
    path('favorite/', FavouriteAdvView.as_view(), name='favourite'),
]
