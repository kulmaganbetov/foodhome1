from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.views.generic.base import View
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView
from account.models import UserSite
from .forms import PhoneNumberForm, SupportForm
from .models import Support, AdditionalData, PhoneNumber, FAQ


# Mixin для передачи url как дополнительный параметр
class UrlMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = self.request.GET.get('url', None)
        return context

# Mixin для отображения сообщении об успешном завершении
class DeleteMixin:

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        data = super().delete(request, *args, **kwargs)
        messages.success(self.request, self.success_message % obj.__dict__)
        return data


# Дополнительные данные создать или обновить
class AdditionalDataCreatOrUpdateView(View):

    def post(self, request, slug):
        user_site = get_object_or_404(
        	UserSite, slug=slug, user=request.user)
        element_id = request.POST.get('element_id')
        photo = request.FILES.get('photo', None)
        value = request.POST.get('value', None)
        obj, created = AdditionalData.objects.get_or_create(
            element_id = element_id,
            user_site=user_site,
            defaults = {
                'value':value, 'element_id': element_id,
                'photo': photo, 'user_site': user_site
            }
        )
        if not created:
            obj.photo = photo
            obj.value = value
            obj.element_id = element_id
            obj.slug = user_site
            obj.save()
        return HttpResponse('saved')



# Создать поддержку клиента
class SupportFormView(LoginRequiredMixin, View):

    def dispatch(self, *args, **kwargs):
        self.support = None
        self.slug = self.kwargs.get('slug')
        self.url = self.request.GET.get('url', None)
        pk = self.kwargs.get('pk', None)
        self.user_site = UserSite.objects.get(
            slug=self.slug, user=self.request.user)
        if pk:
            self.support = get_object_or_404(Support, pk=pk)
        self.PhoneNumberFormSet = modelformset_factory(
            PhoneNumber, form=PhoneNumberForm, 
            extra=1, max_num=1, can_delete=True, min_num=1, validate_min=True
        )
        return super().dispatch(*args, **kwargs)

    def get(self,request, *args, **kwargs):
        form = SupportForm(request, instance=self.support)
        phone_number_formset = self.PhoneNumberFormSet(
            queryset=PhoneNumber.objects.filter(support=self.support),
            prefix="phone_numbers",
            form_kwargs={"request": request},
        )
        return render(request,'support/form.html',
                {'form': form, 'phone_number_formset': phone_number_formset,
                'slug': self.slug, 'url': self.url})

    def post(self,request, *args, **kwargs):
        form = SupportForm(request, data=request.POST, instance=self.support)
        phone_number_formset = self.PhoneNumberFormSet(
            queryset=PhoneNumber.objects.filter(support=self.support),
            data=request.POST,
            prefix="phone_numbers",
            form_kwargs={"request": request},
        )
        if form.is_valid() and phone_number_formset.is_valid():
            instance = form.save(commit=False)
            instance.user_site = self.user_site
            instance.save()
            phone_numbers = phone_number_formset.save(
                commit=False
            )
            for phone_number in phone_numbers:
                phone_number.support = instance
                phone_number.save()
            for phone_number in phone_number_formset.deleted_objects:
                phone_number.delete()
            return redirect(self.user_site.site.construct_url, slug=self.slug)
        return render(request,'support/form.html', 
            {'form': form, 'phone_number_formset': phone_number_formset,
                'slug': self.slug, 'url': self.url})


# Удалить поддержку
class SupportDeleteView(LoginRequiredMixin, UrlMixin, DeleteView):
    model = Support
    template_name = 'support/delete.html'
    success_message = " Кнопка успешно удалена!"

    def get_success_url(self):
        slug = self.kwargs.get('slug')
        user_site = UserSite.objects.get(
            slug=slug, user=self.request.user)
        return reverse_lazy(user_site.site.construct_url, kwargs = {'slug':slug})


# Получить номер поддержки
class SupportPhoneNumber(View):

    def get(self,request, *args, **kwargs):
        support = self.kwargs.get('id')
        support_obj = get_object_or_404(Support, pk=support)
        phone_number_obj = PhoneNumber.objects.filter(
            support=support).order_by('last_date').first()
        if phone_number_obj:
            phone_number_obj.last_date = timezone.now()
            phone_number_obj.save()
            return JsonResponse({
                'status': True,
                'phone_number': phone_number_obj.phone_number,
                'whatsapp_text': support_obj.whatsapp_text
            })
        return JsonResponse({'status': False})


# Mixin категорию
class FAQMixin(SuccessMessageMixin):
    model = FAQ
    fields = ['title', 'description', 'sorting']

    def get_success_url(self):
        slug = self.kwargs.get('slug')
        return reverse_lazy('construct_site_default:construct',
            kwargs = {'slug':slug})


# Mixin редактирования категорию
class FAQEditMixin(FAQMixin, UrlMixin):
    template_name = 'construct_site_default/construct/faq/form.html'

    def form_valid(self, form):
        slug = self.kwargs.get('slug')
        user_site = get_object_or_404(UserSite, slug=slug,
            user=self.request.user)
        obj = form.save(commit=False)
        obj.user_site = user_site
        obj.save()
        return super().form_valid(form)


# Создать категорию
class FAQCreateView(
    LoginRequiredMixin, FAQEditMixin, CreateView):
    success_message = "Ответ успешно добавлен!"


# Обновить категорию
class FAQUpdateView(
    LoginRequiredMixin, FAQEditMixin, UpdateView):
    success_message = "Ответ успешно обновлен!"


# Удалить категорию
class FAQDeleteView(
    LoginRequiredMixin, FAQMixin, DeleteMixin, UrlMixin, DeleteView):
    template_name = 'construct_site_default/construct/faq/delete.html'
    success_message = "Ответ успешно удален!"