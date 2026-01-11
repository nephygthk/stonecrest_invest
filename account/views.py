from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from assets.models import Asset 
from portfolios.models import Portfolio
from portfolios.services import calculate_portfolio_value

def customer_dashboard_view(request):
    return render(request, 'account/customer/dashboard.html', {
        "current_url": request.resolver_match.url_name
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




