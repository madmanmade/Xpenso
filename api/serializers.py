from rest_framework import serializers
from expenses.models import Expense, Category
from userincome.models import UserIncome
from goals.models import FinancialGoal

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ExpenseSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='category', read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    payment_method = serializers.ChoiceField(choices=Expense.PAYMENT_METHODS, default='cash')
    receipt = serializers.FileField(required=False, allow_null=True)
    
    def create(self, validated_data):
        # Use description as title if title is not provided
        if 'description' in validated_data and 'title' not in validated_data:
            validated_data['title'] = validated_data['description'][:200]  # Limit to 200 chars
        return super().create(validated_data)
    
    class Meta:
        model = Expense
        fields = [
            'id', 'amount', 'description', 
            'category', 'category_details', 'date',
            'payment_method', 'receipt', 'owner', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at']
        extra_kwargs = {
            'description': {'required': False},  # Make description optional
            'payment_method': {'write_only': True}  # Hide payment_method in GET responses
        }

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIncome
        fields = ['id', 'amount', 'source', 'date', 'owner']
        read_only_fields = ['owner']

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialGoal
        fields = ['id', 'title', 'target_amount', 'current_amount', 'deadline', 'description', 'user']
        read_only_fields = ['user', 'current_amount']