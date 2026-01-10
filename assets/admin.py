from django.contrib import admin
from .models import Asset

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'asset_type', 'price')
    list_filter = ('asset_type',)
    search_fields = ('symbol', 'name')
