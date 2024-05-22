from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
app_name = 'construct_site_food'

urlpatterns = [
	path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
	path('apply-promocode/', views.ApplyPromoCodeView.as_view(),
		name='apply_promocode'),
	path('<slug:slug>/', views.ClientIndexView.as_view(), name='client'),
	path('<slug:slug>/construct/', views.ConstructIndexView.as_view(),
		name='construct'),
	path('<slug:slug>/good/create/', views.GoodCreateView.as_view(),
		name='good_create'),
	path('<slug:slug>/good/delete/<int:pk>', views.GoodDeleteView.as_view(),
		name='good_delete'),
	path('<slug:slug>/good/update/<int:pk>', views.GoodUpdateView.as_view(),
		name='good_update'),
	path('<slug:slug>/category/create/', views.CategoryCreateView.as_view(),
		name='category_create'),
	path('<slug:slug>/category/delete/<int:pk>', views.CategoryDeleteView.as_view(),
		name='category_delete'),
	path('<slug:slug>/category/update/<int:pk>', views.CategoryUpdateView.as_view(),
		name='category_update'),
	path('good/<int:id>/add/to/cart', views.GoodAddToCart.as_view(),
		name='good_add_to_cart'),
	path('good/<int:id>/remove/from/cart', views.GoodRemoveFromCart.as_view(),
		name='good_remove_from_cart'),
	path('order/page/<slug:slug>', views.OrderView.as_view(),
		name='order_page'),
	path('order/good/', views.OrderGoodView.as_view(),
		name='order_good'),
	path('good/list/<slug:slug>/<int:category>/',
		views.GoodListView.as_view(), name='good_list'),

]

