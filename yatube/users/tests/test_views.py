from django.contrib.auth import get_user_model
from django import forms
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UserPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Ivanov')

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_users_signup_page_uses_correct_template(self):
        """URL-адрес 'users:signup' использует шаблон users/signup.html."""
        response = self.guest_client.get(reverse('users:signup'))
        self.assertTemplateUsed(response, 'users/signup.html')

    def test_signup_page_show_correct_context(self):
        """Шаблон signup сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('users:signup'))
        form_fields = {
            'first_name': forms.fields.CharField,
            'last_name': forms.fields.CharField,
            'username': forms.fields.CharField,
            'email': forms.fields.EmailField,
            'password1': forms.fields.CharField,
            'password2': forms.fields.CharField
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
