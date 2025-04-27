from django.test import TestCase

# Create your tests here.
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Report, ReportCategory
from datetime import datetime

class ReportGenerationTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        
        # Create test category
        self.category = ReportCategory.objects.create(
            name='Test Category',
            description='Test category description'
        )

    def test_report_creation(self):
        """Test creating a new report"""
        response = self.client.post(reverse('create_report'), {
            'title': 'Test Report',
            'category': self.category.id,
            'start_date': datetime.now().date(),
            'end_date': datetime.now().date(),
            'description': 'Test report description'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Report.objects.filter(title='Test Report').exists())

    def test_report_list_view(self):
        """Test viewing list of reports"""
        response = self.client.get(reverse('report_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report_generation/report_list.html')

    def test_report_detail_view(self):
        """Test viewing a specific report"""
        report = Report.objects.create(
            title='Test Report',
            category=self.category,
            created_by=self.user,
            start_date=datetime.now().date(),
            end_date=datetime.now().date(),
            description='Test report description'
        )
        response = self.client.get(reverse('report_detail', args=[report.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report_generation/report_detail.html')

    def test_unauthorized_access(self):
        """Test unauthorized access to reports"""
        self.client.logout()
        response = self.client.get(reverse('report_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        # Test report creation without login
        response = self.client.post(reverse('create_report'), {
            'title': 'Test Report',
            'category': self.category.id,
            'start_date': datetime.now().date(),
            'end_date': datetime.now().date(),
            'description': 'Test report description'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to login

        # Test report detail access without login
        report = Report.objects.create(
            title='Test Report',
            category=self.category,
            created_by=self.user,
            start_date=datetime.now().date(),
            end_date=datetime.now().date(),
            description='Test report description'
        )
        response = self.client.get(reverse('report_detail', args=[report.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect to login
