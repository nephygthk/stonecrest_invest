import random
from decimal import Decimal
from django.db import transaction
from .models import Asset

def simulate_price_changes():
    assets = Asset.objects.all()

    with transaction.atomic():
        for asset in assets:
            change_percent = Decimal(
                random.uniform(
                    -float(asset.volatility),
                    float(asset.volatility)
                )
            )

            multiplier = Decimal('1.00') + (change_percent / Decimal('100'))
            new_price = asset.price * multiplier

            asset.price = max(new_price, Decimal('1.00'))
            asset.save(update_fields=['price'])
