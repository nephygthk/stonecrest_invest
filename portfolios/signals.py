from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Portfolio, PortfolioSnapshot

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_portfolio(sender, instance, created, **kwargs):
    if created:
        Portfolio.objects.create(user=instance)

@receiver(post_save, sender=Portfolio)
def create_initial_snapshot(sender, instance, created, **kwargs):
    if created:
        PortfolioSnapshot.objects.create(
            portfolio=instance,
            total_value=instance.total_value(),
            cash_balance=instance.cash_balance
        )
