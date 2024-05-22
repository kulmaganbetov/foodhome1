from django.urls import path
from . import views
app_name = 'account'

urlpatterns = [
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('authorization/', views.UserAuthorizationView.as_view(), name='authorization'),
    path('<slug:slug>/setting', views.SettingView.as_view(), name='setting'),
]