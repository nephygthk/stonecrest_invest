from django.db import models
from decimal import Decimal
from portfolios.models import Portfolio
from assets.models import Asset

class Trade(models.Model):
    BUY = 'BUY'
    SELL = 'SELL'

    TRADE_TYPES = (
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    )

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name='trades'
    )
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)

    trade_type = models.CharField(
        max_length=4,
        choices=TRADE_TYPES
    )

    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=4
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    executed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trade_type} {self.asset.symbol}"
