from django.contrib.auth import get_user_model

from django.test import Client, TestCase

from ...forms import PostForm
from ...models import Group, Post

User = get_user_model()


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Ivan')
        cls.user2 = User.objects.create_user(username='StasBasov')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )

        cls.post = Post.objects.create(
            author=cls.user,
            text='Текст первого поста',
            group=cls.group,
        )
        number_of_post = 12
        for post_num in range(1, number_of_post + 1):
            cls.post = Post.objects.create(
                author=cls.user,
                text=f'Текст {post_num}',
                group=cls.group)

        cls.form = PostForm()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client2 = Client()
        self.authorized_client2.force_login(self.user2)
