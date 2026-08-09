from django.shortcuts import render
from django.db.models import Sum
from decimal import Decimal
from rest_framework import viewsets
from .models import Expense
from .serializers import ExpenseSerializer
from bap_ops_django.choices import RECORD_TYPE_CHOICES


def expense_list(request):
    record_type_filter = request.GET.get('record_type', '').strip()
    car_only = request.GET.get('car_only', '') == '1'
    sort = request.GET.get('sort', '-date')

    valid_sorts = {'date', '-date', 'amount', '-amount'}
    if sort not in valid_sorts:
        sort = '-date'

    expenses = Expense.objects.all()

    if record_type_filter:
        expenses = expenses.filter(record_type=record_type_filter)
    if car_only:
        expenses = expenses.filter(is_car_expense=True)

    expenses = expenses.order_by(sort)

    total_1099 = Expense.objects.filter(record_type='TAX_1099').aggregate(total=Sum('amount'))['total'] or Decimal('0')
    total_501 = Expense.objects.filter(record_type='NONPROFIT_501').aggregate(total=Sum('amount'))['total'] or Decimal('0')
    total_car = Expense.objects.filter(is_car_expense=True).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    context = {
        'expenses': expenses,
        'record_type_choices': RECORD_TYPE_CHOICES,
        'record_type_filter': record_type_filter,
        'car_only': car_only,
        'sort': sort,
        'total_1099': total_1099,
        'total_501': total_501,
        'total_car': total_car,
    }
    return render(request, 'expenses/expense_list.html', context)


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer