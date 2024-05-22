from django.conf import settings
from django.db import models
from django.utils import timezone
from construct_site_food.models import Good
from decimal import Decimal


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    uses_limit = models.PositiveIntegerField(default=1)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'), blank=True,
                                              null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), blank=True,
                                          null=True)

    def __str__(self):
        return self.code

    def is_valid_for_user(self, user):
        """Проверяет, может ли пользователь использовать этот промокод."""
        if not self.is_active or (self.end_date is not None and self.end_date < timezone.now()):
            return False

        user_usage = self.userpromocodeusage_set.filter(user=user).first()
        if user_usage and user_usage.uses_count >= self.uses_limit:
            return False

        return True

    def use_by_user(self, user):
        """Регистрирует использование промокода пользователем."""
        if self.is_valid_for_user(user):
            user_usage, created = UserPromoCodeUsage.objects.get_or_create(promo_code=self, user=user)
            user_usage.uses_count += 1
            user_usage.save()
            return True
        return False


class UserPromoCodeUsage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE)
    uses_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.promo_code.code}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('accepted', 'Заказ принят'),
        ('in_progress', 'Заказ делается'),
        ('courier', 'Передан курьеру'),
        ('delivered', 'Доставлен'),
        ('arrived', 'Прибыл'),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='accepted')
    delivery_time = models.DateTimeField(default=timezone.now() + timezone.timedelta(minutes=50))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        """Возвращает сумму скидки в зависимости от типа скидки."""
        total_cost = self.get_total_cost_before_discount()
        if self.discount_percentage > 0:
            discount = (self.discount_percentage / Decimal('100.0')) * total_cost
        else:
            discount = self.discount_amount
        return discount.quantize(Decimal('0.01'))

    def get_total_cost(self):
        """Возвращает итоговую стоимость заказа с учетом скидки."""
        total_cost = self.get_total_cost_before_discount()
        discount = self.get_discount()
        return (total_cost - discount).quantize(Decimal('0.01'))


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    good = models.ForeignKey(Good,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return str(self.id)
    def get_cost(self):
        return self.price * self.quantity

