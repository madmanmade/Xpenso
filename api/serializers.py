from rest_framework import serializers
from expenses.models import Expense, Category
from userincome.models import Income
from goals.models import Goal

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ExpenseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    
    class Meta:
        model = Expense
        fields = ['id', 'amount', 'description', 'category', 'date', 'owner']
        read_only_fields = ['owner']

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'amount', 'source', 'date', 'owner']
        read_only_fields = ['owner']

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'title', 'target_amount', 'current_amount', 'deadline', 'description', 'user']
        read_only_fields = ['user', 'current_amount']