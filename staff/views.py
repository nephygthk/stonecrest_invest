from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .decorators import admin_staff_only
from assets.forms import AssetForm
from assets.models import Asset

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
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff:add_asset') 
    else:
        form = AssetForm()
    context = {
        "current_url": request.resolver_match.url_name,
        'form':form,
    }
    return render(request, 'account/admin/add_asset.html', context )
