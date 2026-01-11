import time
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .decorators import admin_staff_only
from assets.forms import AssetForm
from assets.models import Asset
from trading.models import Trade
from strategies.models import Strategy
from strategies import forms 

@login_required
@admin_staff_only
def admin_dashboard_view(request):
    all_assets = Asset.objects.all()

    context = {
        "current_url": request.resolver_match.url_name,
        'all_assets':all_assets
    }
    return render(request, 'account/admin/admin_dashboard.html', context )

@login_required
@admin_staff_only
def add_asset_view(request):
    if request.method == 'POST':
        time.sleep(3)
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Asset is created successfully.")
            return redirect('staff:add_asset') 
    else:
        form = AssetForm()
    context = {
        "current_url": request.resolver_match.url_name,
        'form':form,
    }
    return render(request, 'account/admin/add_asset.html', context )


@login_required
@admin_staff_only
def delete_asset_view(request, asset_id):
    if request.method == "POST":
        time.sleep(2)  # optional delay
        asset = get_object_or_404(Asset, id=asset_id)
        asset.delete()
        messages.success(request, "Asset deleted successfully.")
        return redirect('staff:admin_dashboard')
    

@login_required
@admin_staff_only
def admin_trade_list_view(request):
    trades = Trade.objects.select_related(
        'portfolio',
        'asset'
    ).order_by('-executed_at')

    context = {
        "current_url": request.resolver_match.url_name,
        "trades": trades,
    }
    return render(request, 'account/admin/trade_list.html', context)


@login_required
@admin_staff_only
def admin_strategy_list_view(request):
    strategies = Strategy.objects.prefetch_related(
        'allocations__asset'
    )

    context = {
        "current_url": request.resolver_match.url_name,
        "strategies": strategies,
    }
    return render(
        request,
        'account/admin/strategy_list.html',
        context
    )


@login_required
@admin_staff_only
def admin_strategy_create_view(request):
    if request.method == 'POST':
        form = forms.StrategyForm(request.POST)
        formset = forms.StrategyAllocationFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            strategy = form.save()
            allocations = formset.save(commit=False)

            for allocation in allocations:
                allocation.strategy = strategy
                allocation.save()
            messages.success(request, "Strategy Created successfully.")
            return redirect('staff:admin_strategy_list')
    else:
        form = forms.StrategyForm()
        formset = forms.StrategyAllocationFormSet()

    context = {
        "current_url": request.resolver_match.url_name,
        "form": form,
        "formset": formset,
    }
    return render(
        request,
        'account/admin/strategy_form.html',
        context
    )