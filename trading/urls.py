from django.urls import path, include

from . import views

app_name = 'trading'

urlpatterns = [
    path('test-buy/<int:asset_id>/', views.test_buy_view, name='test_buy'),
]