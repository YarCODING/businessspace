from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main page'),
    path('rooms', views.room_list, name='room_list'),
    path('room/<int:pk>/', views.room_detail, name='room_detail'),
    path('my-bookings/', views.user_bookings, name='user_bookings'),
]