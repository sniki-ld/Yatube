from django.urls import reverse

from posts.tests.my_fixtures.posts_fixture import BaseTest, User


class UserPagesTests(BaseTest):
    def test_new_user_create(self):
        """
        Валидная форма со страницы регистрации
        создаёт новую запись в User.
        """
        self.assertFalse(User.objects.filter(username='StepStep').exists())

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
        self.assertTrue(User.objects.filter(username='StepStep').exists())
