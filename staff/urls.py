from django.urls import path

from . import views

app_name = 'staff'

urlpatterns = [
    path('dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path("add/", views.add_asset_view, name="add_asset"),
    path('delete/<int:asset_id>/', views.delete_asset_view, name='delete_asset'),
    path('trades/', views.admin_trade_list_view, name='admin_trade_list'),
    path('strategies/', views.admin_strategy_list_view,name='admin_strategy_list'),
    path('strategies/create/', views.admin_strategy_create_view,name='admin_strategy_create'),
]