from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from expenses.views import ExpenseViewSet
from donations.views import DonationViewSet
from inventory.views import VaseReceivedViewSet, VaseReturnedViewSet
from auto.views import MileageEntryViewSet
from . import views

router = routers.DefaultRouter()
router.register(r'expenses', ExpenseViewSet)
router.register(r'donations', DonationViewSet)
router.register(r'vases-received', VaseReceivedViewSet)
router.register(r'vases-returned', VaseReturnedViewSet)
router.register(r'mileage', MileageEntryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('expenses/', include('expenses.urls')),
    path('donations/', include('donations.urls')),
    path('inventory/', include('inventory.urls')),
    path('auto/', include('auto.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]