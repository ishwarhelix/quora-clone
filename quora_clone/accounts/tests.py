from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import UserRegistrationForm

# Create your tests here.

class UserRegistrationFormTest(TestCase):
    def test_registration_form_valid_data(self):
        form = UserRegistrationForm({
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertTrue(form.is_valid())

    def test_registration_form_invalid_data(self):
        form = UserRegistrationForm({
            'username': '',
            'email': 'invalid-email',
            'password1': 'short',
            'password2': 'different',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password2', form.errors)

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        
    def test_register_GET(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertIsInstance(response.context['form'], UserRegistrationForm)
        
    def test_register_POST_valid_data(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        
    def test_register_POST_invalid_data(self):
        response = self.client.post(self.register_url, {
            'username': '',
            'email': 'invalid-email',
            'password1': 'pwd1',
            'password2': 'pwd2',
        })
        self.assertEqual(response.status_code, 200)  # Form is displayed again
        self.assertEqual(User.objects.count(), 0)  # No user created
        
class LoginLogoutTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')
        
    def test_login_GET(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        
    def test_login_POST_valid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, self.home_url)
        
    def test_login_POST_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)  # Form is displayed again
        
    def test_logout(self):
        # First login
        self.client.login(username='testuser', password='testpassword123')
        
        # Then logout
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, self.home_url)
