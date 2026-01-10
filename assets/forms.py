from django import forms
from .models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'symbol', 'asset_type', 'price', 'volatility']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter asset name'}),
            'symbol': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter symbol'}),
            'asset_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'volatility': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
