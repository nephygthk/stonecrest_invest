from django.conf import settings
from django.db import models
from decimal import Decimal

from assets.models import Asset

User = settings.AUTH_USER_MODEL

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cash_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('1000000.00')  # virtual money
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def total_value(self):
        holdings_value = sum(
            h.market_value() for h in self.holdings.all()
        )
        return self.cash_balance + holdings_value

    def __str__(self):
        return f"{self.user} Portfolio"
    
    def initial_value(self):
        first = self.snapshots.order_by('created_at').first()
        return first.total_value if first else self.cash_balance

    def current_value(self):
        return self.total_value()

    def total_return(self):
        return self.current_value() - self.initial_value()

    def return_percentage(self):
        initial = self.initial_value()
        if initial == 0:
            return 0
        return (self.total_return() / initial) * 100
    

class Holding(models.Model):
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name='holdings'
    )
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)

    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=4
    )

    average_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('portfolio', 'asset')

    def market_value(self):
        return self.quantity * self.asset.price

    def buy_value(self, amount):
        """
        Buy asset worth `amount` (value-based buy)
        """
        if amount <= 0:
            return

        price = self.asset.price
        quantity_to_buy = amount / price

        if self.portfolio.cash_balance < amount:
            amount = self.portfolio.cash_balance
            quantity_to_buy = amount / price

        self.quantity += quantity_to_buy
        self.portfolio.cash_balance -= amount

        self.save()
        self.portfolio.save()

    def sell_value(self, amount):
        """
        Sell asset worth `amount` (value-based sell)
        """
        if amount <= 0:
            return

        price = self.asset.price
        quantity_to_sell = amount / price

        if quantity_to_sell > self.quantity:
            quantity_to_sell = self.quantity
            amount = quantity_to_sell * price

        self.quantity -= quantity_to_sell
        self.portfolio.cash_balance += amount

        self.save()
        self.portfolio.save()

    def unrealized_pnl(self):
        return (self.asset.price - self.average_price) * self.quantity


class RebalanceLog(models.Model):
    portfolio = models.ForeignKey(
        'Portfolio',
        on_delete=models.CASCADE,
        related_name='rebalances'
    )
    strategy = models.ForeignKey(
        'strategies.Strategy',
        on_delete=models.CASCADE
    )
    executed_at = models.DateTimeField(auto_now_add=True)

    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Rebalance {self.portfolio.id} @ {self.executed_at}"


class DividendLog(models.Model):
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name='dividends'
    )
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.asset.symbol} dividend {self.amount}"


class PortfolioSnapshot(models.Model):
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name='snapshots'
    )
    total_value = models.DecimalField(
        max_digits=14,
        decimal_places=2
    )
    cash_balance = models.DecimalField(
        max_digits=14,
        decimal_places=2
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.portfolio.id} @ {self.created_at}"
