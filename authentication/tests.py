from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile, UserPreference

class UserProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            currency_preference='USD',
            monthly_budget=1000.00
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.currency_preference, 'USD')
        self.assertEqual(float(self.profile.monthly_budget), 1000.00)
        self.assertTrue(self.profile.notification_enabled)

    def test_profile_str_representation(self):
        expected_str = "testuser's profile"
        self.assertEqual(str(self.profile), expected_str)

class UserPreferenceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='prefuser',
            password='prefpass123',
            email='pref@example.com'
        )
        self.preferences = UserPreference.objects.create(
            user=self.user,
            dark_mode=True,
            language='en'
        )

    def test_preference_creation(self):
        self.assertEqual(self.preferences.user.username, 'prefuser')
        self.assertTrue(self.preferences.dark_mode)
        self.assertEqual(self.preferences.language, 'en')
        self.assertTrue(self.preferences.email_notifications)
        self.assertTrue(self.preferences.push_notifications)

    def test_preference_str_representation(self):
        expected_str = "prefuser's preferences"
        self.assertEqual(str(self.preferences), expected_str)

class AuthenticationViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='authuser',
            password='authpass123',
            email='auth@example.com'
        )

    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'authuser',
            'password': 'authpass123'
        })
        self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertEqual(response.status_code, 200)
