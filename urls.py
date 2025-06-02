from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import register, home
urlpatterns = [
    path('', views.home, name='home'),
    path('reserve/<str:slot_id>/', views.reserve_slot, name='reserve_slot'),
    path('cancel/<str:slot_id>/', views.cancel_slot, name='cancel_slot'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
     path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('add-slot/', views.add_slot, name='add_slot'),
    path('delete-slot/<str:slot_id>/', views.delete_slot, name='delete_slot'),
]
