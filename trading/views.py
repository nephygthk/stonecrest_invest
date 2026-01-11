from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from assets.models import Asset
from portfolios.models import Portfolio
from .services import execute_buy

@login_required
def test_buy_view(request, asset_id):
    asset = Asset.objects.get(id=asset_id)
    portfolio = Portfolio.objects.get(user=request.user)

    execute_buy(
        portfolio=portfolio,
        asset=asset,
        quantity=10
    )

    return redirect('account:customer_dashboard')
