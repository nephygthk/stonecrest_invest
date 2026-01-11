from django.shortcuts import render, redirect
from django.contrib import messages

from .tasks import update_prices_task

def manual_price_stimulation(request):
    if request.method == 'POST':
        update_prices_task(request)
        messages.success(request, "Asset prices are stimulated successfully.")
        return redirect('staff:admin_dashboard')

    return render(request, 'assets/manual_price_stimulation.html')
