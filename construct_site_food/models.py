import contextlib
from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill
from account.models import UserSite

# Базовый mixin
class BaseMixin(models.Model):
    title = models.CharField(max_length=180)

    def __str__(self):
        return self.title

    class Meta:
    	abstract = True


# Список категории
class Category(BaseMixin):
    user_site = models.ForeignKey(
    	UserSite, on_delete=models.CASCADE,
    	null=True, blank=True,
    	related_name='category_user_sites')
    color = models.CharField(max_length=120, default="#fc8019")
    sorting = models.IntegerField(default=0)


#Список товаров
class Good(BaseMixin):
    title = models.CharField(max_length=120, null=True, blank=True)
    description = models.TextField(blank=True)
    price = models.CharField(max_length=120, blank=True, default='')
    old_price = models.CharField(max_length=120, blank=True, default='')
    photo = ProcessedImageField(upload_to='images/',
                                processors=[ResizeToFill(317, 231)],
                                format='JPEG',
                                options={'quality': 100})
    category = models.ForeignKey(Category,
    	on_delete=models.SET_NULL, null=True, blank=True)
    user_site = models.ForeignKey(
    	UserSite, on_delete=models.CASCADE,
    	related_name='good_user_sites', null=True, blank=True)
    sorting = models.IntegerField(default=0)
