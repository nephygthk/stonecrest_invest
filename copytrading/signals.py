# copytrading/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from strategies.models import PortfolioStrategy
from .models import CopyRelationship
from .services import copy_leader_strategies_to_follower, check_follower_strategy_health

@receiver(post_save, sender=PortfolioStrategy)
def auto_copy_new_strategy(sender, instance, created, **kwargs):
    """
    When a leader creates a new strategy allocation, copy it to all active followers.
    """
    if not created:
        return  # Only react to new strategies

    leader_portfolio = instance.portfolio

    # Skip if this strategy belongs to a follower (avoid loops)
    if CopyRelationship.objects.filter(follower=leader_portfolio).exists():
        return

    # Get active followers
    active_followers = CopyRelationship.objects.filter(
        leader=leader_portfolio,
        is_active=True
    ).select_related('follower')

    total_leader_cash = instance.allocated_cash

    for relation in active_followers:
        follower_portfolio = relation.follower

        check_follower_strategy_health(follower_portfolio)
        follower_cash = (instance.allocated_cash / total_leader_cash) * relation.allocated_cash

        # Copy the new strategy to follower
        copy_leader_strategies_to_follower(
            leader_portfolio=leader_portfolio,
            follower_portfolio=follower_portfolio,
            allocated_cash=follower_cash
        )
