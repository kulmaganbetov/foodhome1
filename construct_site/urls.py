from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
app_name = 'construct_site'

urlpatterns = [
	path('<slug:slug>/additional/data/create/or/update',
		views.AdditionalDataCreatOrUpdateView.as_view(),
		name='additional_data_creat_or_update'),
	path('<slug:slug>/support/form/', views.SupportFormView.as_view(),
		name='support_form'),
    path('<slug:slug>/support/form/<int:pk>', views.SupportFormView.as_view(),
		name='support_form'),
    path('<slug:slug>/support/delete/<int:pk>', views.SupportDeleteView.as_view(),
		name='support_delete'),
    path('<slug:slug>/support/phone/number/<int:id>', views.SupportPhoneNumber.as_view(),
		name='support_phone_number'),
    path('<slug:slug>/faq/create/',
		views.FAQCreateView.as_view(), name='faq_create'),
	path('<slug:slug>/faq/delete/<int:pk>',
		views.FAQDeleteView.as_view(), name='faq_delete'),
	path('<slug:slug>/faq/update/<int:pk>',
		views.FAQUpdateView.as_view(), name='faq_update'),
]

