from django.views.generic import TemplateView, UpdateView, ListView
from django.http import HttpResponseRedirect
from django.views.generic import View

from apps.adv_board.favourite import Favourite

from .models import Rubric, Category, Advertisement, FavoriteAd
from django.shortcuts import render, get_object_or_404, redirect
from apps.users.models import CustomUser
from .forms import AdverisementModelForm


# Create your views here.

class IndexTemplateView(TemplateView):
    """Главная странница"""
    template_name = 'adv/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # отображение последних 4-х добавленных объявлений
        adv_qs = Advertisement.objects.filter(in_active=True, is_locked=False).order_by('-date_creation')[:4]
        context['adv_list'] = adv_qs
        return context


class RubricListView(ListView):
    """Отобажение всех имеющихся рубрик"""
    template_name = 'rubric/rubric_list.html'
    queryset = Rubric.objects.all()
    context_object_name = 'rubric_list'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['some'] = 'value'
        return context


def rubric_detail(request, slug):
    """Детальное информация о рубрике"""
    context = {}
    rubrics = get_object_or_404(Rubric, slug=slug)
    category_qs = Category.objects.all()
    context['rubrics'] = rubrics
    context['category_list'] = category_qs
    return render(request, 'rubric/rubric_detail.html', context)


class CategoryListView(ListView):
    """Отобажение всех имеющихся категорий"""
    template_name = 'category/category_list.html'
    queryset = Category.objects.all()
    context_object_name = 'category_list'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['some'] = 'value'
        return context


def category_detail(request, slug_rubric, pk):
    """Детальная информация о категории"""
    context = {}
    category_qs = Category.objects.filter(
        pk=pk, rubric_id__slug=slug_rubric
    ).first()
    adv_qs = Advertisement.objects.all()
    context['adv_list'] = adv_qs
    context['category'] = category_qs
    return render(request, 'category/category_detail.html', context)


class AdvertisementListView(ListView):
    """Список объявлений с пагинацией. На одной страние отображается 5 объявлений"""
    template_name = 'adv/adv_list.html'
    queryset = Advertisement.objects.filter(in_active=True, is_locked=False).order_by('-date_creation')
    paginate_by = 5


def adv_detail(request, slug_category, pk):
    """Детальный просмотр объявления"""
    context = {}
    adv_qs = Advertisement.objects.filter(
        pk=pk, id_category__slug=slug_category
    ).first()
    author_qs = CustomUser.objects.filter(pk=pk)
    """Добавляем объявления в "избранные" """
    if request.method == 'POST':
        if request.user.is_authenticated:
            """Для залогиненых пользователей"""
            adv_id = request.POST.get('adv_id')
            ddd = Advertisement.objects.get(pk=adv_id)
            # idd = int(adv_id)
            user = request.user
            id_user = user.pk
            uuu = CustomUser.objects.get(pk=id_user)
            favorite = FavoriteAd.objects.create(id_adv=ddd, id_user=uuu)
            favorite.save()
        else:
            """Для анонимных пользователей"""
            adv_id = request.POST.get('adv_id')
            adv_qs = get_object_or_404(Advertisement, pk=adv_id)
            favourite = Favourite(request)
            favourite.add(adv_qs)
            print(favourite)
    adv_qs.count_view += 1  # счетчик просмотров объявления
    adv_qs.save()
    context['adv_op'] = adv_qs
    context['author'] = author_qs
    return render(request, 'adv/adv_detail.html', context)


class FavouriteAdvView(TemplateView):
    """Отображение "избранных" объявлений для анонимных пользователей"""
    template_name = 'favorite_adv/favo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favourite'] = Favourite(self.request)
        return context


def adv_create(request):
    """Создание объявления(только для зарегистрированных пользователей)"""
    context = {}
    form = AdverisementModelForm()

    if request.method == 'POST':
        form = AdverisementModelForm(request.POST)
        if form.is_valid():
            adv_form = form.save(commit=False)
            adv_form.id_user = request.user
            adv_form.save()
            adv_form.email_send()
            return HttpResponseRedirect('/')
    else:
        context['form'] = form
        return render(request, 'adv/adv_create.html', context)


class AdvEdit(UpdateView):
    """Редактирование объявления(Доступно для автора объявления)"""
    model = Advertisement
    template_name = 'adv/adv_update_form.html'
    fields = ['title', 'description', 'price', 'location_a']
    template_name_suffix = '_update_form.html'


def moderation_list(request):
    """Список не проверенных объявлений, доступен модераторам и админу"""
    context = {}
    adv_moderation = Advertisement.objects.filter(in_active=False, in_moderation=True)
    context['adv_moderation'] = adv_moderation
    return render(request, 'adv/moderation_adv_list.html', context)


class SearchView(ListView):
    """Поиск по сайту"""
    template_name = 'adv/search.html'
    context_object_name = 'adv_list'

    def get_queryset(self):
        return Advertisement.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class HiddenAdvView(View):
    """Срыть обяление(Доступно модераторам и администратору)"""

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        adv_hidden = get_object_or_404(Advertisement, pk=pk)
        adv_hidden.in_active = False
        adv_hidden.save()
        return redirect('adv_board:adv-list')


class PublicationAdvView(View):
    """Опубликовать обяление(Доступно модераторам и администратору)"""

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        publication = get_object_or_404(Advertisement, pk=pk)
        publication.in_active = True
        publication.is_locked = False
        publication.save()
        return redirect('adv_board:moderation-list')


class LockedAdvUserView(View):
    """Заблокировать все обяления пользователя (Доступно модераторам и администратору)"""

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        userr = CustomUser.objects.get(email=pk)
        id_user = userr.pk
        adv_locked = Advertisement.objects.filter(id_user=id_user)
        for adv in adv_locked:
            adv.is_locked = True
            adv.save()
        return redirect('adv_board:adv-list')


class FavoriteTemplateView(TemplateView):
    """Отображение "избранных" объявлений для зарегистрированных пользователей"""
    template_name = 'favorite_adv/favorite_adv.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        pk = user.pk
        context['fav_list'] = FavoriteAd.objects.filter(id_user=pk)
        return context
