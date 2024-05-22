from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from cart.cart import Cart
from construct_site.models import AdditionalData

register = template.Library()

@register.simple_tag
def get_additional_data(element_id, slug):

	additional_data = AdditionalData.objects.filter(
		element_id=element_id, user_site__slug=slug).first()
	if additional_data:
		return additional_data
	else:
		return None


@register.simple_tag
def get_text(element_id, slug, text_default):

	additional_data = AdditionalData.objects.filter(
		element_id=element_id, user_site__slug=slug).first()
	if additional_data:
		return additional_data.value
	else:
		return text_default


@register.simple_tag
def element_present(element_id, slug):
	return AdditionalData.objects.filter(
		element_id=element_id, user_site__slug=slug).exists()


@register.simple_tag
def get_photo(element_id, slug,  photo_default):
	additional_data = AdditionalData.objects.filter(
		element_id=element_id, user_site__slug=slug).first()
	if additional_data:
		return additional_data.photo.url
	else:
		return static(photo_default)

@register.simple_tag
def category_as_list(categories):
	return categories.filter(is_slider=False)

@register.simple_tag
def categories_as_slider(categories):
	return categories.filter(is_slider=True)

@register.simple_tag
def get_good(request, good_id):
	cart = Cart(request)
	return cart.get_good(good_id)

@register.simple_tag
def get_cart(request):
	cart = Cart(request)
	return cart.get_good_ids()

@register.simple_tag
def get_photo_url(element, photo_default):
	if element:
		return element.url
	else:
		return static(photo_default)

@register.simple_tag
def is_selected(val1, val2):
	if str(val1)==str(val2):
		return 'selected'
	else:
		return ''


@register.simple_tag
def is_checked(val1, val2):
	if val1==val2:
		return 'checked'
	else:
		return ''

@register.simple_tag
def condition_set(condition, classes1, classes2, value=''):
	if value == '':
		if condition:
			return classes1
		else:
			return classes2
	else:
		if condition == value:
			return classes1
		else:
			return classes2

@register.simple_tag
def get_category(var1, var2, var3, default):
    if var1==var2:
        return var3
    else: 
        return default


@register.simple_tag
def concate_str(str1, str2):
	return str(str1) + str(str2)


@register.simple_tag
def set_cookie(slug, support):
	return str(slug) + str(support)

@register.simple_tag
def set_style(property, value, condition=True):
	if condition:
		return mark_safe('style="{0}:{1}"'.format(property,value))
	else:
		return ''

@register.simple_tag
def condition_count(condition1, condition2, value=''):
	if condition1 > condition2:
		return value
	return ''
