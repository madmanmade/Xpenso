from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from .models import Source, UserIncome
from django.core.files.uploadedfile import SimpleUploadedFile

class UserIncomeTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Create test source
        self.source = Source.objects.create(
            name='Salary',
            owner=self.user
        )
        
        # Create test income with receipt
        test_receipt = SimpleUploadedFile(
            "test_receipt.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        
        self.income = UserIncome.objects.create(
            amount=Decimal('1000.00'),
            description='Monthly salary',
            source=self.source,
            date='2023-01-01',
            owner=self.user,
            notes='Regular monthly income',
            receipt=test_receipt
        )
        
        self.client = Client()
        
    def test_source_str(self):
        """Test the string representation of Source model"""
        self.assertEqual(str(self.source), 'Salary')
        
    def test_income_str(self):
        """Test the string representation of UserIncome model"""
        self.assertEqual(str(self.income), 'Salary - $1000.00')
        
    def test_income_amount_validation(self):
        """Test that income amount must be positive"""
        with self.assertRaises(Exception):
            UserIncome.objects.create(
                amount=Decimal('-100.00'),
                description='Invalid amount',
                source=self.source,
                date='2023-01-01',
                owner=self.user
            )
            
    def test_income_list_view(self):
        """Test income list view requires login"""
        response = self.client.get(reverse('income'))
        self.assertEqual(response.status_code, 302)  # Redirects to login
        
        # Test after login
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('income'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Monthly salary')
        self.assertContains(response, '$1,000.00')

    def test_add_income(self):
        """Test adding new income with all fields"""
        self.client.login(username='testuser', password='testpass123')
        
        test_receipt = SimpleUploadedFile(
            "bonus_receipt.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        
        data = {
            'amount': '2000.00',
            'description': 'Bonus payment',
            'source': self.source.id,
            'date': '2023-02-01',
            'notes': 'Year-end bonus',
            'receipt': test_receipt
        }
        
        response = self.client.post(reverse('add-income'), data)
        self.assertEqual(response.status_code, 302)  # Redirects after successful creation
        
        # Verify income was created with all fields
        new_income = UserIncome.objects.get(description='Bonus payment')
        self.assertEqual(new_income.amount, Decimal('2000.00'))
        self.assertEqual(new_income.notes, 'Year-end bonus')
        self.assertTrue(new_income.receipt.name.endswith('bonus_receipt.pdf'))
        
    def test_income_permissions(self):
        """Test income permissions"""
        # Create another user
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        
        # Login as other user
        self.client.login(username='otheruser', password='otherpass123')
        
        # Should not be able to view first user's income
        response = self.client.get(
            reverse('edit-income', args=[self.income.id])
        )
        self.assertEqual(response.status_code, 404)
        
        # Should not be able to delete first user's income
        response = self.client.post(
            reverse('delete-income', args=[self.income.id])
        )
        self.assertEqual(response.status_code, 404)
