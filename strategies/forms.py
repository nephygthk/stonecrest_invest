# forms.py
from django import forms
from django.forms import inlineformset_factory

from .models import Strategy, StrategyAllocation

class StrategyForm(forms.ModelForm):
    class Meta:
        model = Strategy
        fields = [
            'name',
            'description',
            'risk_level',
            'target_return_min',
            'target_return_max',
            'is_active',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Strategy name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Short Description'
            }),
            'risk_level': forms.Select(attrs={
                'class': 'form-select'
            }),
            'target_return_min': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 5.00'
            }),
            'target_return_max': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 15.00'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class StrategyAllocationForm(forms.ModelForm):
    class Meta:
        model = StrategyAllocation
        fields = ['asset', 'percentage']
        widgets = {
            'asset': forms.Select(attrs={
                'class': 'form-select'
            }),
            'percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 25.00'
            }),
        }

StrategyAllocationFormSet = inlineformset_factory(
    Strategy,
    StrategyAllocation,
    form=StrategyAllocationForm,
    extra=3,          # ✅ only three inline rows
    can_delete=False  # no JS, keep simple
)
