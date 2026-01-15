from decimal import Decimal
from trading.models import Trade
from .models import CopyRelationship

from decimal import Decimal
from copytrading.models import CopyTradePnL
from trading.models import Trade

def mirror_trade(leader_portfolio, asset, trade_type, quantity):
    """
    Mirror a leader trade to all active followers
    """
    from trading.services import execute_buy, execute_sell

    # Do NOT mirror trades made by followers
    if CopyRelationship.objects.filter(follower=leader_portfolio, is_active=True).exists():
        return

    followers = CopyRelationship.objects.filter(
        leader=leader_portfolio,
        is_active=True
    ).select_related('follower')

    leader_value = leader_portfolio.total_value()

    if leader_value <= 0:
        return

    for relation in followers:
        follower = relation.follower
        # Safety checks
        if follower.id == leader_portfolio.id:
            continue

        follower_value = follower.total_value()
        if follower_value <= 0:
            continue

        # Scale trade proportionally
        ratio = follower_value / leader_value
        follower_quantity = quantity * ratio

        if follower_quantity <= Decimal('0.0001'):
            continue

        pnl_obj, _ = CopyTradePnL.objects.get_or_create(
            follower=follower,
            leader=leader_portfolio
        )

        try:
            if trade_type == Trade.BUY:
                execute_buy(
                    portfolio=follower,
                    asset=asset,
                    quantity=follower_quantity,
                    note="Copy trade buy"
                )
                pnl_obj.total_invested += asset.price * follower_quantity

            elif trade_type == Trade.SELL:
                execute_sell(
                    portfolio=follower,
                    asset=asset,
                    quantity=follower_quantity,
                    note="Copy trade sell"
                )
                pnl_obj.total_realized_pnl += asset.price * follower_quantity

            pnl_obj.save()

        except Exception:
            # Fail silently so leader trade is never blocked
            continue
