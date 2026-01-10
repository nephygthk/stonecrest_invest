from django.db import models
from decimal import Decimal

class Asset(models.Model):
    ASSET_TYPES = (
        ('STOCK', 'Stock'),
        ('ETF', 'ETF'),
        ('REIT', 'REIT'),
    )

    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=20, unique=True)
    asset_type = models.CharField(max_length=10, choices=ASSET_TYPES)

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('100.00')
    )

    volatility = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('1.50')
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} ({self.asset_type})"
