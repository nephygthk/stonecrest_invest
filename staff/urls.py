from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path("add/", views.add_asset_view, name="add_asset"),
    path('delete/<int:asset_id>/', views.delete_asset_view, name='delete_asset'),
]