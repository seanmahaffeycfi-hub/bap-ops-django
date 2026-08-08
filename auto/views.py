from django.shortcuts import render
from django.db.models import Sum, F
from decimal import Decimal
from .models import MileageEntry


def mileage_dashboard(request):
    available_years = sorted(
        {entry.date.year for entry in MileageEntry.objects.all()},
        reverse=True
    )
    default_year = available_years[0] if available_years else None

    try:
        selected_year = int(request.GET.get('year', default_year))
    except (TypeError, ValueError):
        selected_year = default_year

    entries = MileageEntry.objects.all()
    if selected_year:
        entries = entries.filter(date__year=selected_year)
    entries = entries.order_by('-date')

    entries_with_miles = [
        {
            'date': e.date,
            'start_mileage': e.start_mileage,
            'end_mileage': e.end_mileage,
            'miles': e.miles_driven,
            'record_type': e.get_record_type_display(),
        }
        for e in entries
    ]

    year_entries = MileageEntry.objects.filter(date__year=selected_year) if selected_year else MileageEntry.objects.none()
    total_1099 = Decimal('0')
    total_501 = Decimal('0')
    for e in year_entries:
        if e.record_type == 'TAX_1099':
            total_1099 += e.miles_driven
        else:
            total_501 += e.miles_driven

    context = {
        'entries': entries_with_miles,
        'available_years': available_years,
        'selected_year': selected_year,
        'total_1099': total_1099,
        'total_501': total_501,
    }
    return render(request, 'auto/mileage_dashboard.html', context)

from rest_framework import viewsets
from .serializers import MileageEntrySerializer


class MileageEntryViewSet(viewsets.ModelViewSet):
    queryset = MileageEntry.objects.all()
    serializer_class = MileageEntrySerializer