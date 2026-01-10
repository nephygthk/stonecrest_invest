from decimal import Decimal
from portfolios.models import Holding, RebalanceLog

def calculate_portfolio_value(portfolio):
    holdings_value = sum(
        h.market_value() for h in portfolio.holdings.all()
    )
    return portfolio.cash_balance + holdings_value


def calculate_holdings_value(portfolio):
    return sum(
        h.market_value() for h in portfolio.holdings.all()
    )


def rebalance_portfolio(portfolio):
    strategy = portfolio.strategy
    total_value = portfolio.total_value()

    for allocation in strategy.allocations.select_related('asset'):
        target_value = (
            Decimal(allocation.percentage) / 100
        ) * total_value

        holding, _ = Holding.objects.get_or_create(
            portfolio=portfolio,
            asset=allocation.asset,
            defaults={'quantity': 0}
        )

        current_value = holding.market_value()
        difference = target_value - current_value

        if abs(difference) < Decimal('1.00'):
            continue  # ignore tiny drift

        if difference > 0:
            holding.buy_value(difference)
        else:
            holding.sell_value(abs(difference))

    RebalanceLog.objects.create(
        portfolio=portfolio,
        strategy=strategy,
        notes="Automated daily rebalance"
    )