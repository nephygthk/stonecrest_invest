from decimal import Decimal
from portfolios.models import Portfolio, PortfolioSnapshot, Holding, RebalanceLog, DividendLog
from strategies.models import PortfolioStrategy

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
    """
    Rebalance a single portfolio based on its assigned strategy
    """
    try:
        portfolio_strategy = PortfolioStrategy.objects.select_related(
            'strategy'
        ).get(portfolio=portfolio)
    except PortfolioStrategy.DoesNotExist:
        return  # portfolio has no strategy, skip

    strategy = portfolio_strategy.strategy
    total_value = portfolio.total_value()

    for allocation in strategy.allocations.select_related('asset'):
        target_value = (
            Decimal(allocation.percentage) / Decimal('100')
        ) * total_value

        holding, _ = Holding.objects.get_or_create(
            portfolio=portfolio,
            asset=allocation.asset,
            defaults={'quantity': 0}
        )

        current_value = holding.market_value()
        difference = target_value - current_value

        # Ignore very small drift
        if abs(difference) < Decimal('1.00'):
            continue

        if difference > 0:
            holding.buy_value(difference)
        else:
            holding.sell_value(abs(difference))

    RebalanceLog.objects.create(
        portfolio=portfolio,
        strategy=strategy,
        notes="Automated strategy rebalance"
    )




def pay_reit_dividends():
    reit_holdings = Holding.objects.filter(
        asset__asset_type='REIT',
        quantity__gt=0
    ).select_related('asset', 'portfolio')

    for holding in reit_holdings:
        asset = holding.asset

        if not asset.annual_yield:
            continue

        if asset.dividend_frequency == 'MONTHLY':
            period_yield = asset.annual_yield / Decimal('12')
        else:
            period_yield = asset.annual_yield / Decimal('4')

        dividend_amount = (
            holding.market_value() * period_yield / Decimal('100')
        )

        if dividend_amount <= 0:
            continue

        holding.portfolio.cash_balance += dividend_amount
        holding.portfolio.save()

        DividendLog.objects.create(
            portfolio=holding.portfolio,
            asset=asset,
            amount=dividend_amount
        )


def take_daily_snapshots():
    portfolios = Portfolio.objects.all()

    for portfolio in portfolios:
        PortfolioSnapshot.objects.create(
            portfolio=portfolio,
            total_value=portfolio.total_value(),
            cash_balance=portfolio.cash_balance
        )