from random import randint
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateResponseMixin, View
from django.template.defaultfilters import slugify
from django.contrib.auth import authenticate, login, logout
from construct_site.models import Support, PhoneNumber 
from .models import Site, UserSite
from .forms import UserRegistrationForm, UserSiteForm


# Mixin для передачи url как дополнительный параметр
class UrlMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = self.request.GET.get('url', None)
        return context


# Mixin сайта
class SiteMixinView(View):

    def dispatch(self, *args, **kwargs):
        slug = 'food'
        self.site = get_object_or_404(Site, slug=slug)
        return super().dispatch(*args, **kwargs)


# Создать настройку
class SettingView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'setting/index.html'

    def dispatch(self, *args, **kwargs):
        self.slug = self.kwargs.get('slug')
        self.user_site = UserSite.objects.get(
            slug=self.slug, user=self.request.user)
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        user_site_form = UserSiteForm(instance=self.user_site)
        return self.render_to_response(
            {'slug': self.slug, 'user_site_form': user_site_form})

    def post(self, request, *args, **kwargs):
        user_site_form = UserSiteForm(
            request.POST, request.FILES, instance=self.user_site)
        if user_site_form.is_valid():
            user_site=user_site_form.save(commit=False)
            user_site.slug = self.slug
            user_site.user = request.user
            user_site.save()
            return redirect('account:setting', slug=self.slug)
        return self.render_to_response(
            {'slug': self.slug, 'user_site_form': user_site_form})

# Регистрация пользователя
class UserRegistrationView(TemplateResponseMixin, SiteMixinView):
    template_name = 'registration/registration.html' 

    def get(self,request):
        registration_form = UserRegistrationForm()
        return self.render_to_response(
            {'registration_form': registration_form})

    def post(self, request):
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            phone_number = registration_form.cleaned_data['phone_number']
            new_user=registration_form.save(commit=False)
            new_user.set_password(
                registration_form.cleaned_data['password']
            )
            new_user.save()
            authenticate_user = authenticate(
                username=registration_form.cleaned_data['username'],
                password=registration_form.cleaned_data['password']
            )
            login(request, authenticate_user)
            user = request.user
            site_slug = slugify(user.username)
            user_site = UserSite(site=self.site, user=user)
            slug_exists = UserSite.objects.filter(slug=site_slug).exists()
            if slug_exists:
                extra = str(randint(1, 10000))
                site_slug = slugify(user.username) + extra
            user_site.slug = site_slug
            user_site.company_name = user.username
            user_site.phone_number = phone_number
            user_site.save()
            support = Support.objects.create(
                user_site=user_site, is_main=True)
            PhoneNumber.objects.create(support=support, phone_number=phone_number)
            return redirect(self.site.construct_url, slug=site_slug)
        return self.render_to_response(
            {'registration_form': registration_form})


# Авторизация пользователя
class UserAuthorizationView(View):

    def get(self,request):
        user_site = get_object_or_404(UserSite, user=request.user)
        return redirect(user_site.site.construct_url, slug=user_site.slug)


