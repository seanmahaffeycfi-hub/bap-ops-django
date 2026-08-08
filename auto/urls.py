from django.urls import path
from . import views

urlpatterns = [
    path('', views.mileage_dashboard, name='mileage_dashboard'),
]