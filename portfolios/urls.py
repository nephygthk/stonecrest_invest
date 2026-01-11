from django.urls import path
from . import views

app_name = 'portfolio'
urlpatterns = [
    path('rebalance/', views.rebalance_all_portfolios, name='rebalance'),
    path('run-dividends/', views.run_dividends, name='run_dividends'),
]