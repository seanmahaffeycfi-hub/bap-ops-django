from django.shortcuts import render
from django.db.models import Sum
from decimal import Decimal
from .models import Donation


def donation_list(request):
    sort = request.GET.get('sort', '-date')
    valid_sorts = {'date', '-date', 'value', '-value'}
    if sort not in valid_sorts:
        sort = '-date'

    donations = Donation.objects.all().order_by(sort)
    total_value = Donation.objects.aggregate(total=Sum('value'))['total'] or Decimal('0')

    context = {
        'donations': donations,
        'sort': sort,
        'total_value': total_value,
    }
    return render(request, 'donations/donation_list.html', context)

from rest_framework import viewsets
from .serializers import DonationSerializer


class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer