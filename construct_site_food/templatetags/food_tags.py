from django import template
from construct_site_food.models import Good

register = template.Library()

@register.simple_tag
def get_food_good(id):
	try:
		good = Good.objects.get(id=id)
	except Good.DoesNotExist:
		good = None
	return good