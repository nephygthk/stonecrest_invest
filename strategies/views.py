from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ValidationError
from django.contrib import messages

from portfolios.models import Portfolio
from .models import Strategy, PortfolioStrategy
from .services import execute_strategy, strategy_average_return, switch_strategy

@login_required
def activate_strategy_view(request, strategy_id):
    portfolio = Portfolio.objects.get(user=request.user)
    strategy = get_object_or_404(Strategy, id=strategy_id)

    if hasattr(portfolio, 'portfoliostrategy'):
        # User already has a strategy → SWITCH
        try:
            switch_strategy(portfolio, strategy)
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('strategies:list')
    else:
        # First time → APPLY
        PortfolioStrategy.objects.create(
            portfolio=portfolio,
            strategy=strategy
        )
        execute_strategy(portfolio, strategy)

    return redirect('account:portfolio')


@login_required
def strategy_list_view(request):
    strategies = Strategy.objects.filter(is_active=True)
    return render(request, 'account/customer/strategies/list.html', {
        'strategies': strategies
    })


@login_required
def strategy_leaderboard(request):
    strategies = Strategy.objects.filter(is_active=True)

    leaderboard = []
    for strategy in strategies:
        leaderboard.append({
            'strategy': strategy,
            'avg_return': strategy_average_return(strategy),
            'asset_types': ", ".join(strategy.asset_types()),
        })

    leaderboard.sort(
        key=lambda x: x['avg_return'],
        reverse=True
    )

    return render(
        request,
        'account/customer/strategies/leaderboard.html',
        {'leaderboard': leaderboard}
    )

