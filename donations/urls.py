from django.urls import path
from . import views

urlpatterns = [
    path('', views.donation_list, name='donation_list'),
]