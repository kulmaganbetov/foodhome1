from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
	url('', include('pwa.urls')),
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(
    	redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/', include('account.urls')),
    path('construct/site/', include('construct_site.urls')),
    path('', include('construct_site_food.urls')),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, 
		                 document_root=settings.MEDIA_ROOT)
