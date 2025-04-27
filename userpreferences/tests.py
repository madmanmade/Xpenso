from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserPreference
from django.contrib.messages import get_messages

class TestUserPreferences(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
    def test_preferences_page_get(self):
        response = self.client.get(reverse('preferences'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'preferences/index.html')
        
    def test_save_preferences(self):
        data = {
            'currency': 'USD'
        }
        response = self.client.post(reverse('preferences'), data)
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(str(messages[0]), 'Preferences saved successfully')
        
        # Verify preference was saved
        preference = UserPreference.objects.get(user=self.user)
        self.assertEqual(preference.currency, 'USD')
