from django.shortcuts import render


def inventory_dashboard(request):
    return render(request, 'inventory/inventory_dashboard.html', {})