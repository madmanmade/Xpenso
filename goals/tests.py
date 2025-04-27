from django.test import TestCase

# Create your tests here.
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Goal

class GoalTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()
        
        # Create a test goal
        self.goal = Goal.objects.create(
            user=self.user,
            title='Test Goal',
            target_amount=1000.00,
            current_amount=0.00,
            deadline='2024-12-31'
        )

    def test_goal_creation(self):
        """Test if goal is created correctly"""
        self.assertEqual(self.goal.title, 'Test Goal')
        self.assertEqual(self.goal.target_amount, 1000.00)
        self.assertEqual(self.goal.current_amount, 0.00)
        
    def test_goal_list_view(self):
        """Test goal list view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('goals:goal-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Goal')

    def test_goal_detail_view(self):
        """Test goal detail view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('goals:goal-detail', args=[self.goal.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Goal')

    def test_goal_update(self):
        """Test goal update functionality"""
        self.client.login(username='testuser', password='testpass123')
        updated_data = {
            'title': 'Updated Goal',
            'target_amount': 2000.00,
            'current_amount': 500.00,
            'deadline': '2024-12-31'
        }
        response = self.client.post(
            reverse('goals:goal-update', args=[self.goal.id]),
            updated_data
        )
        self.goal.refresh_from_db()
        self.assertEqual(self.goal.title, 'Updated Goal')
        self.assertEqual(self.goal.target_amount, 2000.00)

    def test_goal_delete(self):
        """Test goal deletion"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('goals:goal-delete', args=[self.goal.id]))
        self.assertEqual(Goal.objects.count(), 0)
    def test_goal_progress(self):
        """Test goal progress calculation"""
        self.client.login(username='testuser', password='testpass123')
        
        # Add progress record
        progress = GoalProgress.objects.create(
            goal=self.goal,
            amount_added=250.00,
            notes="Test progress"
        )
        
        self.goal.current_amount = 250.00
        self.goal.save()
        
        # Test progress percentage
        self.assertEqual(self.goal.progress, 25.0)
        
        # Test progress record creation
        self.assertEqual(GoalProgress.objects.count(), 1)
        self.assertEqual(progress.amount_added, 250.00)

    def test_goal_achievability(self):
        """Test goal achievability calculation"""
        # Create income for user
        Income.objects.create(
            user=self.user,
            average_monthly_income=3000.00
        )
        
        # Test achievable goal
        self.goal.current_amount = 500.00
        self.goal.save()
        self.assertTrue(self.goal.is_achievable())
        
        # Test unachievable goal
        self.goal.target_amount = 100000.00
        self.goal.save()
        self.assertFalse(self.goal.is_achievable())

    def test_goal_reminder(self):
        """Test goal reminder functionality"""
        reminder = GoalReminder.objects.create(
            goal=self.goal,
            reminder_date=timezone.now().date() + timezone.timedelta(days=5),
            message="Test reminder"
        )
        
        # Test reminder creation
        self.assertTrue(reminder.is_active)
        self.assertTrue(reminder.is_due_soon())
        
        # Test reminder deactivation
        reminder.mark_as_inactive()
        self.assertFalse(reminder.is_active)
        
        # Test reminder rescheduling
        new_date = timezone.now().date() + timezone.timedelta(days=10)
        reminder.reschedule(new_date)
        self.assertEqual(reminder.reminder_date, new_date)
