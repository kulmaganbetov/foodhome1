from django.contrib import admin
from .models import PromoCode, UserPromoCodeUsage, Order, OrderItem

class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'uses_limit', 'start_date', 'end_date', 'is_active', 'discount_percentage', 'discount_amount']
    list_filter = ['is_active', 'start_date', 'end_date']
    search_fields = ['code']

admin.site.register(PromoCode, PromoCodeAdmin)

class UserPromoCodeUsageAdmin(admin.ModelAdmin):
    list_display = ['user', 'promo_code', 'uses_count']
    list_filter = ['user', 'promo_code']
    search_fields = ['user__username', 'promo_code__code']

admin.site.register(UserPromoCodeUsage, UserPromoCodeUsageAdmin)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['good']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'address', 'created', 'updated', 'paid', 'get_total_cost']
    list_filter = ['paid', 'created', 'updated']
    search_fields = ['user__username', 'address']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'good', 'price', 'quantity', 'get_cost']
    search_fields = ['order__id', 'good__name']

admin.site.register(OrderItem, OrderItemAdmin)
