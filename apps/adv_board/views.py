from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView, ListView
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import View


from .models import Rubric, Category, Advertisement, FavoriteAd
from django.shortcuts import render, get_object_or_404, redirect
from apps.users.models import CustomUser
from .forms import AdverisementModelForm
from random import randint


# Create your views here.

class IndexTemplateView(TemplateView):
    template_name = 'adv/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        adv_qs = Advertisement.objects.filter(in_active=True, is_locked=False).order_by('-date_creation')[:4]
        context['adv_list'] = adv_qs
        return context


def rubric_list(request):
    context = {}
    rubric_qs = Rubric.objects.all()
    context['rubric_list'] = rubric_qs
    return render(request, 'rubric/rubric_list.html', context)


def rubric_detail(request, slug):
    context = {}
    rubrics = get_object_or_404(Rubric, slug=slug)
    category_qs = Category.objects.all()
    context['rubrics'] = rubrics
    context['category_list'] = category_qs
    return render(request, 'rubric/rubric_detail.html', context)


def category_list(request):
    context = {}
    category_qs = Category.objects.all()
    context['category_list'] = category_qs
    return render(request, 'category/category_list.html', context)


def category_detail(request, slug_rubric, pk):
    context = {}
    category_qs = Category.objects.filter(
        pk=pk, rubric_id__slug=slug_rubric
    ).first()
    adv_qs = Advertisement.objects.all()
    context['adv_list'] = adv_qs
    context['category'] = category_qs

    return render(request, 'category/category_detail.html', context)


class AdvertisementListView(ListView):
    template_name = 'adv/adv_list.html'
    queryset = Advertisement.objects.filter(in_active=True, is_locked=False).order_by('-date_creation')
    paginate_by = 5


def adv_detail(request, slug_category, pk):
    context = {}
    adv_qs = Advertisement.objects.filter(
        pk=pk, id_category__slug=slug_category
    ).first()
    author_qs = CustomUser.objects.filter(pk=pk)
    if request.method == 'POST':
        adv_id = request.POST.get('adv_id')
        ddd = Advertisement.objects.get(pk=adv_id)
        idd = int(adv_id)
        user = request.user
        id_user = user.pk
        uuu = CustomUser.objects.get(pk=id_user)
        favorite = FavoriteAd.objects.create(id_adv=ddd, id_user=uuu)
        favorite.save()
    adv_qs.count_view += 1
    adv_qs.save()
    context['adv_op'] = adv_qs
    context['author'] = author_qs
    return render(request, 'adv/adv_detail.html', context)


def adv_create(request):
    context = {}
    form = AdverisementModelForm()

    if request.method == 'POST':
        form = AdverisementModelForm(request.POST)
        if form.is_valid():
            adv_form = form.save(commit=False)
            adv_form.id_user = request.user
            adv_form.save()
            return HttpResponseRedirect('/')
    else:
        context['form'] = form
        return render(request, 'adv/adv_create.html', context)


class AdvEdit(UpdateView):
    model = Advertisement
    template_name = 'adv/adv_update_form.html'
    fields = ['title', 'description', 'price']
    template_name_suffix = '_update_form.html'


def moderation_list(request):
    context = {}
    adv_moderation = Advertisement.objects.filter(in_active=False, in_moderation=True)
    context['adv_moderation'] = adv_moderation
    return render(request, 'adv/moderation_adv_list.html', context)


class SearchView(ListView):
    template_name = 'adv/search.html'
    context_object_name = 'adv_list'

    def get_queryset(self):
        return Advertisement.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class HiddenAdvView(View):

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        adv_hidden = get_object_or_404(Advertisement, pk=pk)
        adv_hidden.in_active = False
        adv_hidden.save()
        return redirect('adv_board:adv-list')


class PublicationAdvView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        publication = get_object_or_404(Advertisement, pk=pk)
        publication.in_active = True
        publication.is_locked = False
        publication.save()
        return redirect('adv_board:moderation-list')


class LockedAdvUserView(View):

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
    template_name = 'favorite_adv/favorite_adv.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        pk = user.pk
        context['fav_list'] = FavoriteAd.objects.filter(id_user=pk)
        return context

