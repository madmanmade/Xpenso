from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category, Expense
from .serializers import CategorySerializer, ExpenseSerializer
from decimal import Decimal
from datetime import date

class CategoryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Food')

    def test_create_category(self):
        url = reverse('category-list')
        data = {'name': 'Transportation'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.get(name='Transportation').name, 'Transportation')

    def test_get_categories(self):
        url = reverse('category-list')
        response = self.client.get(url)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ExpenseTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Food')
        self.expense = Expense.objects.create(
            title='Lunch',
            description='Restaurant lunch',
            amount=Decimal('15.50'),
            date=date.today(),
            category=self.category,
            user=self.user
        )

    def test_create_expense(self):
        url = reverse('expense-list')
        data = {
            'title': 'Dinner',
            'description': 'Evening meal',
            'amount': '25.00',
            'date': date.today().isoformat(),
            'category': self.category.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 2)

    def test_get_expenses(self):
        url = reverse('expense-list')
        response = self.client.get(url)
        expenses = Expense.objects.filter(user=self.user)
        serializer = ExpenseSerializer(expenses, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_expense(self):
        url = reverse('expense-detail', args=[self.expense.id])
        data = {
            'title': 'Updated Lunch',
            'amount': '20.00',
            'date': date.today().isoformat(),
            'category': self.category.id
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.expense.refresh_from_db()
        self.assertEqual(self.expense.title, 'Updated Lunch')
        self.assertEqual(self.expense.amount, Decimal('20.00'))

    def test_delete_expense(self):
        url = reverse('expense-detail', args=[self.expense.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Expense.objects.count(), 0)
