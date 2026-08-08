from django.shortcuts import render


def mileage_dashboard(request):
    return render(request, 'auto/mileage_dashboard.html', {})