from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),

    path('register/', views.register, name='register'),

    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('checkout/',views.checkout,name='checkout'),
    path('orders/',views.my_orders,name='orders'),
    path(
    'increase/<int:id>/',
    views.increase_quantity,
    name='increase_quantity'
),

path(
    'decrease/<int:id>/',
    views.decrease_quantity,
    name='decrease_quantity'
),

path(
    'wishlist/',
    views.wishlist,
    name='wishlist'
),

path(
    'wishlist/add/<int:id>/',
    views.add_to_wishlist,
    name='add_to_wishlist'
),

path(
    'wishlist/remove/<int:id>/',
    views.remove_from_wishlist,
    name='remove_from_wishlist'
),
]