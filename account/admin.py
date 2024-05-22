from django.contrib import admin
from .models import Site, UserSite

admin.site.register(Site)
admin.site.register(UserSite)
