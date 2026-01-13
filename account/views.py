from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from assets.models import Asset 
from portfolios.models import Portfolio
from portfolios.services import calculate_portfolio_value

def customer_dashboard_view(request):
    portfolio = Portfolio.objects.get(user=request.user)
    holdings = portfolio.holdings.select_related('asset')
    snapshots = portfolio.snapshots.order_by('created_at')
    holding_count = portfolio.holdings.count()

    # Aggregate by asset type
    allocation = {}
    for holding in holdings:
        asset_type = holding.asset.asset_type
        allocation.setdefault(asset_type, 0)
        allocation[asset_type] += holding.market_value()

    # ✅ Convert dict → lists
    allocation_labels = list(allocation.keys())
    allocation_values = [float(v) for v in allocation.values()]

    # Recent trades
    trades = portfolio.trades.all()[:10]

    snapshot_labels = [s.created_at.strftime("%Y-%m-%d") for s in snapshots]
    snapshot_values = [float(s.total_value) for s in snapshots]

    if len(snapshots) >= 2:
        today_value = snapshots.last().total_value
        yesterday_value = snapshots.reverse()[1].total_value  # second last
        print(today_value)
        print(yesterday_value)
        todays_pnl = today_value - yesterday_value
        print(todays_pnl)
        todays_pnl_percent = (todays_pnl / yesterday_value) * 100
    else:
        todays_pnl = 0
        todays_pnl_percent = 0

    # -------------------------------
    # Calculate ROI
    # ROI = (current value - starting cash) / starting cash * 100
    # -------------------------------
    starting_cash = snapshots.first().cash_balance if snapshots.exists() else portfolio.cash_balance
    current_value = portfolio.total_value()
    roi_percent = ((current_value - starting_cash) / starting_cash) * 100 if starting_cash > 0 else 0

    return render(request, 'account/customer/dashboard.html', {
        "current_url": request.resolver_match.url_name,
        'portfolio': portfolio,
        'holding_count': holding_count,
        'allocation_labels': allocation_labels,
        'allocation_values': allocation_values,
        'trades': trades,
        'snapshot_labels': snapshot_labels,
        'snapshot_values': snapshot_values,
        'todays_pnl': todays_pnl,
        'todays_pnl_percent': round(todays_pnl_percent, 2),
        'roi_percent': round(roi_percent, 2),
    })


@login_required
def portfolio_view(request):
    portfolio = Portfolio.objects.get(user=request.user)
    total_value = calculate_portfolio_value(portfolio)
    
    return render(request, "account/customer/portfolio.html", {
        "current_url": request.resolver_match.url_name,
        'portfolio': portfolio,
        'total_value': total_value,
    })

def assets_view(request):
    assets = Asset.objects.all().order_by('asset_type', 'symbol')
    return render(request, "account/customer/assets.html", {
        "current_url": request.resolver_match.url_name,
        'assets': assets
    })

def asset_detail(request, symbol):
    # asset = get_object_or_404(Asset, symbol=symbol)

    return render(request, "account/customer/asset_detail.html", {
        # "asset": asset,
        "current_url": "assets"
    })

def stocks_view(request):
    return render(request, "account/customer/stocks.html", {
        "current_url": request.resolver_match.url_name
    })

def stock_detail_view(request):
    return render(request, "account/customer/stock_detail.html", {
        "current_url": "stocks"
    })

    
def reits_view(request):
    return render(request, "account/customer/reits.html", {
        "current_url": request.resolver_match.url_name
    })

def reit_detail_view(request):
    return render(request, "account/customer/reit_detail.html", {
        "current_url": "reits"
    })

def copy_trading_view(request):
    return render(request, "account/customer/copy_trading.html", {
        "current_url": "copy_trading"
    })

def wallet_view(request):
    return render(request, "account/customer/wallet.html", {
        "current_url": "wallet"
    })


@login_required
def trade_history_view(request):
    portfolio = Portfolio.objects.get(user=request.user)
    trades = portfolio.trades.all()
    return render(request, 'account/customer/trade_history.html', {'trades': trades, "current_url": request.resolver_match.url_name,})




