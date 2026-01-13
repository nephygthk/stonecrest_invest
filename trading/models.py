from django.db import models
from decimal import Decimal
from portfolios.models import Portfolio
from assets.models import Asset

# trading/models.py
class Trade(models.Model):
    BUY = 'BUY'
    SELL = 'SELL'
    DIVIDEND = 'DIVIDEND'
    REBALANCE = 'REBALANCE'
    SWITCH = 'SWITCH'

    TRADE_TYPE_CHOICES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
        (DIVIDEND, 'Dividend'),
        (REBALANCE, 'Rebalance'),
        (SWITCH, 'Strategy Switch')
    ]

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='trades')
    asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True, blank=True)
    trade_type = models.CharField(max_length=20, choices=TRADE_TYPE_CHOICES)
    quantity = models.DecimalField(max_digits=20, decimal_places=6)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    total_value = models.DecimalField(max_digits=20, decimal_places=2)
    note = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def save(self, *args, **kwargs):
        if self.trade_type == Trade.DIVIDEND:
            self.total_value = self.price  # dividend cash
        else:
            self.total_value = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.trade_type} {self.asset} {self.total_value}"

