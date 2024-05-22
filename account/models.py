from django.db import models
from django.http import JsonResponse
from django.contrib.auth.models import User


# Список сайтов
class Site(models.Model):
    title = models.CharField(max_length=120)
    construct_url = models.CharField(max_length=120)
    template_name = models.CharField(max_length=380)
    slug = models.SlugField(max_length=120, unique=True)

    def __str__(self):
        return self.title


# Списки сайтов, выбранные пользователем
class UserSite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=120, unique=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)