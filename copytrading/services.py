from decimal import Decimal
from trading.models import Trade
from .models import CopyRelationship

from copytrading.models import CopyTradePnL
from trading.models import Trade
from strategies.models import PortfolioStrategy



def copy_leader_strategies_to_follower(leader_portfolio, follower_portfolio, allocated_cash):
    """
    Copy all active leader strategies to the follower.
    Each follower strategy receives cash proportionally.
    """
    from strategies.services import execute_strategy

    active_strategies = leader_portfolio.strategy_allocations.filter(status='ACTIVE')
    total_leader_cash = sum(ps.allocated_cash for ps in active_strategies)

    if total_leader_cash <= 0:
        return  # Nothing to copy

    for leader_ps in active_strategies:
        # Allocate proportional follower cash
        follower_cash = (leader_ps.allocated_cash / total_leader_cash) * allocated_cash

        # Create follower PortfolioStrategy
        follower_ps, created = PortfolioStrategy.objects.get_or_create(
            portfolio=follower_portfolio,
            strategy=leader_ps.strategy,
            status='ACTIVE',
            defaults={'allocated_cash': follower_cash}
        )

        if not created:
            # If already exists (from previous copy), just update allocated cash
            follower_ps.allocated_cash = follower_cash
            follower_ps.status = 'ACTIVE'
            follower_ps.save(update_fields=['allocated_cash', 'status'])

        # Execute strategy for follower using their allocated cash
        execute_strategy(
            portfolio=follower_portfolio,
            strategy_allocation=follower_ps
        )

def check_follower_strategy_health(follower_portfolio):
    """
    Check all follower strategies and stop any that have depleted allocated cash.
    """
    for ps in follower_portfolio.strategy_allocations.filter(status='ACTIVE'):
        if ps.allocated_cash <= 0 or ps.portfolio.cash_balance <= 0:
            # Stop strategy safely
            ps.status = 'STOPPED'
            ps.save(update_fields=['status'])

            # Liquidate any holdings from this strategy
            from portfolios.services import unwind_strategy_holdings
            unwind_strategy_holdings(follower_portfolio, ps)



            
# def mirror_trade(leader_portfolio, asset, trade_type, quantity):
#     """
#     Mirror a leader trade to all active followers
#     """
#     from trading.services import execute_buy, execute_sell

#     # Do NOT mirror trades made by followers
#     if CopyRelationship.objects.filter(follower=leader_portfolio, is_active=True).exists():
#         return

#     followers = CopyRelationship.objects.filter(
#         leader=leader_portfolio,
#         is_active=True
#     ).select_related('follower')

#     leader_value = leader_portfolio.total_value()

#     if leader_value <= 0:
#         return

#     for relation in followers:
#         follower = relation.follower
#         # Safety checks
#         if follower.id == leader_portfolio.id:
#             continue

#         follower_value = follower.total_value()
#         if follower_value <= 0:
#             continue

#         # Scale trade proportionally
#         ratio = follower_value / leader_value
#         follower_quantity = quantity * ratio

#         if follower_quantity <= Decimal('0.0001'):
#             continue

#         pnl_obj, _ = CopyTradePnL.objects.get_or_create(
#             follower=follower,
#             leader=leader_portfolio
#         )

#         try:
#             if trade_type == Trade.BUY:
#                 execute_buy(
#                     portfolio=follower,
#                     asset=asset,
#                     quantity=follower_quantity,
#                     note="Copy trade buy"
#                 )
#                 pnl_obj.total_invested += asset.price * follower_quantity

#             elif trade_type == Trade.SELL:
#                 execute_sell(
#                     portfolio=follower,
#                     asset=asset,
#                     quantity=follower_quantity,
#                     note="Copy trade sell"
#                 )
#                 pnl_obj.total_realized_pnl += asset.price * follower_quantity

#             pnl_obj.save()

#         except Exception:
#             # Fail silently so leader trade is never blocked
#             continue
