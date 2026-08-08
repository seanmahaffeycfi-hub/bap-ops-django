from django.shortcuts import render
from django.db.models import Sum, Min
from .models import VaseReceived, VaseReturned


def inventory_dashboard(request):
    total_received = VaseReceived.objects.aggregate(total=Sum('quantity'))['total'] or 0
    total_returned = VaseReturned.objects.aggregate(total=Sum('quantity'))['total'] or 0
    vases_out = total_received - total_returned

    # Per-recipient breakdown: how many each person currently holds,
    # ordered by the oldest date they first received vases.
    received_by_recipient = (
        VaseReceived.objects
        .values('recipient')
        .annotate(received_qty=Sum('quantity'), earliest_date=Min('date_received'))
    )
    returned_by_person = {
        row['returned_from']: row['returned_qty']
        for row in VaseReturned.objects.values('returned_from').annotate(returned_qty=Sum('quantity'))
    }

    breakdown = []
    for row in received_by_recipient:
        recipient = row['recipient']
        received_qty = row['received_qty']
        returned_qty = returned_by_person.get(recipient, 0)
        net = received_qty - returned_qty
        if net > 0:
            breakdown.append({
                'recipient': recipient,
                'net_held': net,
                'earliest_date': row['earliest_date'],
            })
    breakdown.sort(key=lambda r: r['earliest_date'])

    context = {
        'total_received': total_received,
        'total_returned': total_returned,
        'vases_out': vases_out,
        'breakdown': breakdown,
        # "Lost or broken vases" was specified in the original requirements but no field
        # exists yet on either the Android or Django side to track condition/loss.
        # This is a known, intentional gap — not a bug. See PROJECT_STATUS.md.
        'lost_or_broken_tracked': False,
    }
    return render(request, 'inventory/inventory_dashboard.html', context)