from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from expenses.models import Expense, Category
from userincome.models import Income
from goals.models import Goal
from .serializers import ExpenseSerializer, CategorySerializer, IncomeSerializer, GoalSerializer

# Create your views here.

class ExpenseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer
    
    def get_queryset(self):
        return Expense.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class IncomeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = IncomeSerializer
    
    def get_queryset(self):
        return Income.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class GoalViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalSerializer
    
    def get_queryset(self):
        return Goal.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_category(request):
    description = request.data.get('description', '')
    # Add category prediction logic here
    predictions = [{'category': 'Sample', 'probability': 0.9}]
    return Response({'predictions': predictions})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_report(request):
    # Add report generation logic here
    report_id = 'sample_report_id'
    return Response({'report_id': report_id})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_forecast(request):
    # Add forecast generation logic here
    forecast_data = {
        'forecast': [],
        'confidence_interval': []
    }
    return Response(forecast_data)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expense_statistics(request):
    """Get statistical summary of user's expenses"""
    user_expenses = Expense.objects.filter(user=request.user)
    
    total_expenses = user_expenses.aggregate(total=Sum('amount'))['total'] or 0
    avg_expense = user_expenses.aggregate(avg=Avg('amount'))['avg'] or 0
    expense_count = user_expenses.count()
    
    # Get expenses by month
    monthly_expenses = user_expenses.annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        total=Sum('amount')
    ).order_by('month')
    
    return Response({
        'total_expenses': total_expenses,
        'average_expense': avg_expense,
        'expense_count': expense_count,
        'monthly_trend': monthly_expenses
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expenses_by_category(request):
    """Get expenses grouped by category"""
    category_expenses = Expense.objects.filter(user=request.user).values(
        'category__name'
    ).annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    return Response(category_expenses)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_expenses(request):
    """Get expenses for each month"""
    year = request.query_params.get('year', datetime.now().year)
    monthly_data = Expense.objects.filter(
        user=request.user,
        date__year=year
    ).annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        total=Sum('amount')
    ).order_by('month')
    
    return Response(monthly_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_summary(request):
    """Get summary of all categories with their expense counts and totals"""
    summary = Category.objects.annotate(
        expense_count=Count('expense'),
        total_amount=Sum('expense__amount', filter=Q(expense__user=request.request.user))
    ).values('id', 'name', 'expense_count', 'total_amount')
    
    return Response(summary)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def income_statistics(request):
    """Get statistical summary of user's income"""
    user_income = Income.objects.filter(owner=request.user)
    
    total_income = user_income.aggregate(total=Sum('amount'))['total'] or 0
    avg_income = user_income.aggregate(avg=Avg('amount'))['avg'] or 0
    income_count = user_income.count()
    
    monthly_income = user_income.annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        total=Sum('amount')
    ).order_by('month')
    
    return Response({
        'total_income': total_income,
        'average_income': avg_income,
        'income_count': income_count,
        'monthly_trend': monthly_income
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def goal_progress(request):
    """Get progress summary of user's financial goals"""
    user_goals = Goal.objects.filter(user=request.user)
    
    goals_summary = user_goals.annotate(
        progress_percentage=ExpressionWrapper(
            F('current_amount') * 100.0 / F('target_amount'),
            output_field=FloatField()
        ),
        remaining_amount=F('target_amount') - F('current_amount'),
        days_remaining=ExpressionWrapper(
            F('deadline') - datetime.now().date(),
            output_field=DurationField()
        )
    ).values('id', 'title', 'target_amount', 'current_amount', 
             'progress_percentage', 'remaining_amount', 'days_remaining')
    
    return Response(goals_summary)
