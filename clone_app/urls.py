from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='clone-home'),
    path('city-search/', views.city, name='clone-city'),
    path('search/', views.search, name='city-search'),
]