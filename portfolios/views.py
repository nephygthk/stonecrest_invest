from django.http import JsonResponse
from .services import rebalance_portfolio, pay_reit_dividends
from portfolios.models import Portfolio


def rebalance_all_portfolios(request):
    portfolios = Portfolio.objects.filter(
        portfoliostrategy__isnull=False
    ).select_related('portfoliostrategy__strategy')

    for portfolio in portfolios:
        rebalance_portfolio(portfolio)

    return JsonResponse({"status": "ok"})


def run_dividends(request):
    pay_reit_dividends()
    return JsonResponse({"status": "dividends paid"})

