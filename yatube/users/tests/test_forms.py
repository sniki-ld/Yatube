from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UserPagesTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_new_user_create(self):
        """
        Валидная форма со страницы регистрации
        создаёт новую запись в User.
        """
        users_count = User.objects.count()
        form_data = {
            'username': 'StepStep',
            'password1': '12345stepan',
            'password2': '12345stepan'
        }
        response = self.guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True)

        self.assertRedirects(response, reverse('posts:index'))
        self.assertEqual(User.objects.count(), users_count + 1)
