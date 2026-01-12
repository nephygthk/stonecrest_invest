from decimal import Decimal
from trading.services import execute_buy
from portfolios.models import Portfolio

def execute_strategy(portfolio, strategy):
    allocations = strategy.allocations.all()
    cash = portfolio.cash_balance

    for allocation in allocations:
        amount_to_invest = (
            allocation.percentage / Decimal('100')
        ) * cash

        asset = allocation.asset
        price = asset.price

        quantity = amount_to_invest / price

        if quantity > 0:
            execute_buy(
                portfolio=portfolio,
                asset=asset,
                quantity=quantity
            )


def strategy_average_return(strategy):
    portfolios = Portfolio.objects.filter(
        portfoliostrategy__strategy=strategy
    )

    returns = [
        p.return_percentage()
        for p in portfolios
        if p.initial_value() and p.initial_value() >= 1000
    ]

    return sum(returns) / len(returns) if returns else 0

