from django import forms
from .models import SavingsGoal

class SavingsGoalForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg shadow-sm',
            'placeholder': 'Enter goal title',
            'style': 'border-radius: 25px;'
        })
    )
    
    target_amount = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter target amount',
            'step': '0.01'
        })
    )
    
    current_amount = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter current savings (optional)',
            'step': '0.01'
        })
    )
    
    period = forms.ChoiceField(
        choices=SavingsGoal.PERIOD_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg shadow-sm',
            'style': 'border-radius: 25px;'
        })
    )
    
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control form-control-lg shadow-sm',
            'type': 'date',
            'style': 'border-radius: 25px;'
        })
    )
    
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control form-control-lg shadow-sm',
            'type': 'date',
            'style': 'border-radius: 25px;'
        })
    )
    
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control form-control-lg shadow-sm',
            'placeholder': 'Enter goal description (optional)',
            'style': 'border-radius: 15px;',
            'rows': 3
        })
    )
    
    class Meta:
        model = SavingsGoal
        fields = ['title', 'target_amount', 'current_amount', 'period', 'start_date', 'end_date', 'description']
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        target_amount = cleaned_data.get('target_amount')
        current_amount = cleaned_data.get('current_amount', 0)
        
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date must be after start date")
        
        if target_amount and target_amount <= 0:
            raise forms.ValidationError("Target amount must be greater than zero")
        
        if current_amount and current_amount < 0:
            raise forms.ValidationError("Current amount cannot be negative")
        
        return cleaned_data 