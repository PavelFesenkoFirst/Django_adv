from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic import FormView, TemplateView, RedirectView
from django.urls import reverse_lazy
from django.views.generic import UpdateView

# Create your views here.
from apps.users.forms import RegisterForm
from apps.adv_board.models import Advertisement
from apps.users.models import CustomUser

class LoginView(FormView):
    """Вход на сайт"""
    form_class = AuthenticationForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:profile')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('adv_board:index')

class LogoutView(RedirectView):
    """Выход"""
    pattern_name = 'adv_board:index'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


class ProfileView(TemplateView):
    """Личный кабинет"""
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        pk = user.pk
        adv_qs = Advertisement.objects.filter(id_user=pk)
        context['adv_con'] = adv_qs
        return context


class RegisterView(FormView):
    """Регистрация на сайте"""
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('adv_board:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class ChangeName(UpdateView):
    """Редактирование имени пользователя"""
    model = CustomUser
    template_name = 'users/name_update_form.html'
    fields = ['name', 'surname']


class ChangeCity(UpdateView):
    """Редактирование города в профиле"""
    model = CustomUser
    template_name = 'users/city_update_form.html'
    fields = ['location']

