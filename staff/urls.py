from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path("add-asset/", views.add_asset_view, name="add_asset"),
]