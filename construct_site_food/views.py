import base64
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView
from django.views.generic.base import TemplateResponseMixin, View
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from account.models import UserSite
from construct_site.models import Support, AdditionalData
from cart.forms import CartAddProductForm
from cart.cart import Cart
from .models import Good, Category
from django.utils import timezone
from cart.models import PromoCode, Order, OrderItem, UserPromoCodeUsage
from .forms import GoodForm
from decimal import Decimal


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

# Mixin товара
class GoodMixin(SuccessMessageMixin):
    model = Good
    form_class = GoodForm

    def get_success_url(self):
        slug = self.kwargs.get('slug')
        kwargs = {'slug': slug}
        return reverse_lazy('construct_site_food:construct', kwargs = kwargs)


# Mixin редактирования товара
class GoodEditMixin(GoodMixin, UrlMixin):
    template_name = 'construct_site_food/construct/good/form.html'

    def form_valid(self, form):
        slug = self.kwargs.get('slug')
        user_site = get_object_or_404(UserSite, slug=slug, user=self.request.user)
        obj = form.save(commit=False)
        obj.user_site = user_site
        obj.save()
        return super().form_valid(form)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        slug = self.kwargs.get('slug')
        form.fields['category'].queryset = Category.objects.filter(
            user_site__slug=slug)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



# Создать товар
class GoodCreateView(LoginRequiredMixin, GoodEditMixin, CreateView):
    success_message = "Товар успешно добавлен!"


# Обновить товар
class GoodUpdateView(LoginRequiredMixin, GoodEditMixin, UpdateView):
    success_message = "Товар успешно обновлен!"


# Удалить товар
class GoodDeleteView(
    LoginRequiredMixin,GoodMixin, UrlMixin, DeleteMixin, DeleteView):
    template_name = 'construct_site_food/construct/good/delete.html'
    success_message = "Товар успешно удален!"


# Mixin категорию
class CategoryMixin(SuccessMessageMixin):
    model = Category
    fields = ['title', 'sorting', 'color']

    def get_success_url(self):
        slug = self.kwargs.get('slug')
        return reverse_lazy('construct_site_food:construct', kwargs = {'slug':slug})


# Mixin редактирования категорию
class CategoryEditMixin(CategoryMixin, UrlMixin):
    template_name = 'construct_site_food/construct/category/form.html'

    def form_valid(self, form):
        slug = self.kwargs.get('slug')
        user_site = get_object_or_404(UserSite, slug=slug, user=self.request.user)
        obj = form.save(commit=False)
        obj.user_site = user_site
        obj.save()
        return super().form_valid(form)

# Создать категорию
class CategoryCreateView(
    LoginRequiredMixin, CategoryEditMixin, CreateView):
    success_message = "Категория успешно добавлена!"


# Обновить категорию
class CategoryUpdateView(
    LoginRequiredMixin, CategoryEditMixin, UpdateView):
    success_message = "Категория успешно обновлена!"


# Удалить категорию
class CategoryDeleteView(
    LoginRequiredMixin, CategoryMixin, DeleteMixin, UrlMixin, DeleteView):
    template_name = 'construct_site_food/construct/category/delete.html'
    success_message = "Категория успешно удалена!"

# Дополнительные данные создать или обновить
class AdditionalDataCreatOrUpdateView(View):

    def post(self, request, slug):
        user_site = get_object_or_404(UserSite, slug=slug, user=request.user)
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


# Дополнительные данные удалить
class AdditionalDataDelete(LoginRequiredMixin, View):

    def post(self, request, slug):
        element_id = request.POST.get('element_id')
        AdditionalData.objects.filter(element_id=element_id,
        	user_site__slug=slug).delete()
        return HttpResponse('deleted')


# Страница конструктора
class ConstructIndexView(LoginRequiredMixin, GoodMixin, ListView):
    template_name = 'construct_site_food/construct/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        category = self.kwargs.get('category', None)
        user_site = get_object_or_404(
            UserSite, slug=slug, user=self.request.user)
        categories = Category.objects.filter(user_site__slug=slug)
        goods = Good.objects.filter(user_site__slug=slug)
        supports = Support.objects.filter(user_site__slug=slug)
        context['user_site'] = user_site
        context['slug'] = slug
        context['categories'] = categories
        context['goods'] = goods
        context['supports'] = supports
        
        return context


# Страница клиента
class ClientIndexView(GoodMixin, View):

    def get(self, request, **kwargs):
        context = {}
        slug = self.kwargs.get('slug')
        categories = Category.objects.filter(
            user_site__slug=slug).select_related().order_by('-sorting')
        supports = Support.objects.filter(user_site__slug=slug)
        goods = Good.objects.filter(user_site__slug=slug).order_by('-sorting')
        if categories.exists():
            category = self.kwargs.get('category', None)
            if not  category:
                category = categories.first().id
            goods = goods.filter(category=category)
            context['active_category'] = category
        user_site = get_object_or_404(UserSite, slug=slug)
        context['slug'] = slug
        context['categories'] = categories
        context['goods'] = goods
        context['supports'] = supports
        context['user_site'] = user_site
        context['manifest_file'] = '/manifest/' + str(slug) + '.json'
        return render(request, user_site.site.template_name, context)


class GoodToCartMixin(View):

    def dispatch(self, *args, **kwargs):
        good_id = self.kwargs.get('id')
        self.cart = Cart(self.request)
        self.good = get_object_or_404(Good, id=good_id)
        return super().dispatch(*args, **kwargs)

# товарить товар в корзину
class GoodAddToCart(GoodToCartMixin):

    def post(self, request, *args, **kwargs):
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            self.cart.add(product=self.good,
                quantity=cd['quantity'],
                decrement=cd['decrement'])
            if self.cart.get_good(self.good):
                quantity = self.cart.get_good(self.good).get('quantity')
            else:
                quantity = 0
            return JsonResponse({
                'status': True,
                'quantity': quantity,
                'total_items': self.cart.get_items(),
                'total_price': self.cart.get_total_price()

            })
        return JsonResponse({'status': False})


# товарить товар в корзину
class GoodRemoveFromCart(GoodToCartMixin):

    def post(self, request, *args, **kwargs):
        self.cart.remove(self.good)
        return JsonResponse({'status': True})


# страница заказа
class OrderView(TemplateResponseMixin, View):
    template_name = 'construct_site_food/foodoma/order.html'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        return self.render_to_response({'slug': slug})

    def post(self, request, *args, **kwargs):
        return self.render_to_response({})

# заказать товар
class OrderGoodView(View):

    def post(self, request, *args, **kwargs):
        delivery_address = request.POST.get('delivery_address', '')
        promocode_code = request.POST.get('promocode', '')
        user = request.user
        cart = Cart(request)

        # Проверка и применение промокода
        discount_amount = Decimal('0.00')
        if promocode_code:
            try:
                promocode = PromoCode.objects.get(code=promocode_code, is_active=True, start_date__lte=timezone.now(),
                                                  end_date__gte=timezone.now())
                if promocode.is_valid_for_user(user):
                    promocode.use_by_user(user)
                    if promocode.discount_percentage:
                        discount_amount = Decimal(promocode.discount_percentage) / Decimal(
                            '100.0') * cart.get_total_price()
                    else:
                        discount_amount = promocode.discount_amount
            except PromoCode.DoesNotExist:
                return JsonResponse({"error": "Недействительный промокод"}, status=400)

        # Создание заказа
        order = Order.objects.create(user=user, address=delivery_address, discount_amount=discount_amount)

        # Создание элементов заказа
        for item in cart:
            good = Good.objects.get(id=item['id'])  # предполагаем, что товар уже проверен на существование
            OrderItem.objects.create(order=order, good=good, price=item['price'], quantity=item['quantity'])

        # Очистка корзины
        cart.clear()

        return JsonResponse({"success": "Заказ успешно создан"})


# Страница клиента
class GoodListView(GoodMixin, ListView):
    context_object_name = 'goods'

    def get_template_names(self):
        template = self.request.GET.get(
            'template', 'construct_site_food/foodoma/good/list.html')
        return [template]

    def get_queryset(self):
        qs = super().get_queryset()
        slug = self.kwargs.get('slug')
        category = self.kwargs.get('category', None)
        qs = qs.filter(user_site__slug=slug).order_by('-sorting')
        if category:
            qs = qs.filter(category=category)
        return qs

from decimal import Decimal

class ApplyPromoCodeView(View):

    def get(self, request, *args, **kwargs):
        promo_code_str = request.GET.get('promocode')
        total_cost = request.GET.get('total_sum')
        total_cost = int(total_cost)
        if not promo_code_str:
            return JsonResponse({"discount": "Промокод не предоставлен."}, status=400)

        try:
            promo_code = PromoCode.objects.get(code=promo_code_str, is_active=True)
        except PromoCode.DoesNotExist:
            return JsonResponse({"discount": "Промокод недействителен или не существует."}, status=404)

        if promo_code.discount_percentage > 0:
            discount = (promo_code.discount_percentage / Decimal('100.0')) * total_cost
        else:
            discount = promo_code.discount_amount
        discount = discount.quantize(Decimal('0.01'))
        price_with_discount = total_cost - discount
        text = price_with_discount
        return JsonResponse({"discount": text})


class OrderListView(ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'construct_site_food/foodoma/order/order_list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created')

from django.views.generic.detail import DetailView
class OrderDetailView(DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'construct_site_food/foodoma/order/order_detail.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)