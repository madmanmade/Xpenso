from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Expense, ExpenseCategory
from decimal import Decimal

class ExpenseTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test category
        self.category = ExpenseCategory.objects.create(
            name='Test Category',
            user=self.user
        )
        
        # Create test expense
        self.expense = Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('50.00'),
            description='Test Expense',
            date='2023-01-01'
        )
        
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')

    def test_expense_creation(self):
        """Test expense creation"""
        self.assertEqual(self.expense.amount, Decimal('50.00'))
        self.assertEqual(self.expense.description, 'Test Expense')
        self.assertEqual(self.expense.user, self.user)

    def test_expense_list_view(self):
        """Test expense list view"""
        response = self.client.get(reverse('expense-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Expense')

    def test_expense_detail_view(self):
        """Test expense detail view"""
        response = self.client.get(reverse('expense-detail', args=[self.expense.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Expense')
        self.assertContains(response, '50.00')

    def test_expense_create_view(self):
        """Test expense creation view"""
        response = self.client.post(reverse('expense-create'), {
            'category': self.category.id,
            'amount': '75.00',
            'description': 'New Test Expense',
            'date': '2023-01-02'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Expense.objects.filter(description='New Test Expense').exists())

    def test_expense_update_view(self):
        """Test expense update view"""
        response = self.client.post(
            reverse('expense-update', args=[self.expense.id]),
            {
                'category': self.category.id,
                'amount': '100.00',
                'description': 'Updated Test Expense',
                'date': '2023-01-01'
            }
        )
        self.expense.refresh_from_db()
        self.assertEqual(self.expense.amount, Decimal('100.00'))
        self.assertEqual(self.expense.description, 'Updated Test Expense')

    def test_expense_delete_view(self):
        """Test expense deletion"""
        response = self.client.post(reverse('expense-delete', args=[self.expense.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Expense.objects.filter(id=self.expense.id).exists())
