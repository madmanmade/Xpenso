from django import forms
from .models import Expense, Category, Budget
from django.conf import settings

class ExpenseForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg shadow-sm',
            'placeholder': 'Enter expense title',
            'style': 'border-radius: 25px;'
        })
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter amount'
        })
    )
    description = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg shadow-sm',
            'placeholder': 'Enter expense description (optional)',
            'style': 'border-radius: 25px;'
        })
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control form-control-lg shadow-sm',
            'type': 'date',
            'style': 'border-radius: 25px;'
        })
    )
    category = forms.ModelChoiceField(
        queryset=None,
        empty_label="Select Category",
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg shadow-sm',
            'style': 'border-radius: 25px;'
        })
    )
    payment_method = forms.ChoiceField(
        choices=Expense.PAYMENT_METHODS,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg shadow-sm',
            'style': 'border-radius: 25px;'
        })
    )
    
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'description', 'category', 'date', 'payment_method', 'receipt']
        exclude = ['owner', 'created_at', 'updated_at']
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(owner=user)
    
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero")
        if amount > settings.MAX_EXPENSE_AMOUNT:
            raise forms.ValidationError(f"Amount cannot exceed {settings.MAX_EXPENSE_AMOUNT}")
        return amount

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3})
        }

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'period', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'})
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(owner=user)
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date must be after start date")