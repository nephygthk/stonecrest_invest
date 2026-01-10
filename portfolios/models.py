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
