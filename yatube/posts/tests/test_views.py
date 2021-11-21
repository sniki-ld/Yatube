from django import forms
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.urls import reverse
from ..models import Follow, Post

from ..tests.my_fixtures.posts_fixture import BaseTest, User


class PostPagesTests(BaseTest):
    def test_pages_uses_correct_template(self):
        """ Во view-функциях используют соответствующие шаблоны."""
        pages = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug': 'test-slug'}): 'posts/group_list.html',
            reverse('posts:profile',
                    kwargs={'username': 'Ivan'}): 'posts/profile.html',
            reverse('posts:post_detail',
                    kwargs={'post_id': '1'}): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/post_create.html',
            reverse('posts:post_edit',
                    kwargs={'post_id': '1'}): 'posts/post_create.html'
        }

        for page, template in pages.items():
            with self.subTest(page=page):
                response = self.authorized_client.get(page)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом: списком постов."""

        response = self.authorized_client.get(
            reverse('posts:index') + '?page=2')
        first_object = response.context['page_obj'][2]
        post_author_0 = first_object.author
        post_text_0 = first_object.text
        post_group_0 = first_object.group.slug

        self.assertEqual(post_author_0, self.user)
        self.assertEqual(post_text_0, 'Текст первого поста')
        self.assertEqual(post_group_0, 'test-slug')

    def test_group_list_pages_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом:
        списком постов, отфильтрованных по группе."""
        response = (self.authorized_client.get(
            reverse('posts:group_list',
                    kwargs={'slug': 'test-slug'}) + '?page=2'))
        first_object = response.context['page_obj'][2]
        post_author_0 = first_object.author
        post_text_0 = first_object.text
        post_group_0 = first_object.group.slug

        self.assertEqual(post_author_0, self.user)
        self.assertEqual(post_text_0, 'Текст первого поста')
        self.assertEqual(post_group_0, 'test-slug')

    def test_profile_pages_show_correct_context(self):
        """
        Шаблон profile сформирован с правильным контекстом:
        списком постов, отфильтрованных по пользователю.
        """
        response = (self.authorized_client.
                    get(reverse('posts:profile',
                                kwargs={'username': 'Ivan'}) + '?page=2'))
        first_object = response.context['page_obj'][2]
        post_author_0 = first_object.author
        post_text_0 = first_object.text
        post_group_0 = first_object.group.slug

        self.assertEqual(post_author_0, self.user)
        self.assertEqual(post_text_0, 'Текст первого поста')
        self.assertEqual(post_group_0, 'test-slug')

    def test_post_detail_pages_show_correct_context(self):
        """
        Шаблон post_detail сформирован с правильным контекстом:
        один пост отфильтрованный по id.
        """
        response = (self.authorized_client.
                    get(reverse('posts:post_detail', kwargs={'post_id': '1'})))
        self.assertEqual(response.context.get('post').text,
                         'Текст первого поста')
        self.assertEqual(response.context.get('post').author,
                         self.user)
        self.assertEqual(response.context.get('post').group.slug,
                         'test-slug')

    def test_create_page_show_correct_context(self):
        """
        Шаблон post_create сформирован с правильным контекстом:
        форма создания поста.
        """
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_create_edit_page_show_correct_context(self):
        """
        Шаблон post_create сформирован с правильным контекстом:
        форма редактирования поста, отфильтрованного по id.
        """
        response = self.authorized_client.get(reverse('posts:post_edit',
                                                      kwargs={'post_id': '1'}))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_group_list_pages_show_correct_group_post(self):
        """Пост соответствует выбранной группе."""
        response = (self.authorized_client.
                    get(reverse('posts:group_list',
                                kwargs={'slug': 'test-slug'})))
        post = response.context['page_obj'][0]
        post_group_title = post.group.title
        group_title = response.context['group'].title
        self.assertEqual(group_title, post_group_title)
        self.assertIn(post, response.context['page_obj'])

    def test_post_is_not_included_in_group_list_pages(self):
        """Пост не соответствует выбранной группе."""
        post_1 = Post.objects.create(
            author=self.user,
            text='Текст поста без группы'
        )

        response = (self.authorized_client.
                    get(reverse('posts:group_list',
                                kwargs={'slug': 'test-slug'})))
        self.assertNotIn(post_1, response.context['page_obj'])
        response = self.authorized_client.get(
            str(reverse('posts:group_list',
                        kwargs={'slug': 'test-slug'}) + '?page=2'))
        self.assertNotIn(post_1, response.context['page_obj'])

    def test_post_with_group_is_on_pages(self):
        """Пост с группой есть на страницах."""
        pages = ['/', '/group/test-slug/', '/profile/Ivan/']
        for page in pages:
            with self.subTest(page=page):
                response = self.authorized_client.get(page)
                post = response.context['page_obj'][0]
                self.assertTrue(post.group)
                self.assertIn(post, response.context['page_obj'])

    def test_cache_page_index(self):
        """Проверка кеширования главной страницы"""
        res_before_del = self.authorized_client.get(
            str(reverse('posts:index') + '?page=2'))
        content_page_before = res_before_del.content
        Post.objects.filter(pk=1).delete()
        res_after_del = self.authorized_client.get(
            str(reverse('posts:index') + '?page=2'))
        content_page_after = res_after_del.content
        self.assertEqual(content_page_before, content_page_after)

        cache.clear()
        res_after_cache_del = self.authorized_client.get(
            str(reverse('posts:index') + '?page=2'))
        content_page_after_cache_del = res_after_cache_del.content
        self.assertNotEqual(content_page_before,
                            content_page_after_cache_del)

    def test_subscription(self):
        """
        Авторизованный пользователь
        может подписываться на других пользователей.
        """
        follow_count = Follow.objects.count()
        author = get_object_or_404(User, username='Ivan')
        Follow.objects.create(
            user=self.user2, author=author)
        self.assertEqual(Follow.objects.count(),
                         follow_count + 1)

    def test_subscription_anonymous(self):
        """
        Анонимный пользователь не может
        подписываться на других пользователей.
        """
        response = (self.client.get(
            reverse('posts:profile_follow',
                    kwargs={'username': 'Ivan'}),
            follow=True))
        self.assertRedirects(response,
                             '/auth/login/?next=/profile/Ivan/follow/')

    def test_unsubscribe(self):
        """
        Авторизованный пользователь может
        удалять других пользователей из подписок.
        """
        before_creation_count = Follow.objects.count()
        author = get_object_or_404(User, username='Ivan')
        Follow.objects.create(user=self.user2, author=author)
        after_creation_count = Follow.objects.count()
        unfollow = Follow.objects.get(user=self.user2, author=author)
        unfollow.delete()
        after_deletion_count = Follow.objects.count()

        self.assertFalse(before_creation_count, after_creation_count)
        self.assertEqual(before_creation_count, after_deletion_count)
        self.assertEqual(Follow.objects.count(), after_deletion_count)

    def test_new_record_if_signed(self):
        """
        Новая запись пользователя появляется в ленте тех, кто на него подписан.
        """
        author = get_object_or_404(User, username='Ivan')
        Follow.objects.create(user=self.user2, author=author)
        post = Post.objects.create(
            author=author,
            text='Пост для подписки')
        response = (self.authorized_client2.
                    get(reverse('posts:follow_index')))
        first_object = response.context['page_obj'][0]
        post_author_0 = first_object.author
        post_text_0 = first_object.text

        self.assertEqual(post_author_0, author)
        self.assertEqual(post_text_0, 'Пост для подписки')
        self.assertIn(post, response.context['page_obj'])

    def test_no_new_record_if_not_signed(self):
        """
        Новая запись пользователя не появляется
        в ленте тех, кто на него не подписан.
        """
        author = get_object_or_404(User, username='Ivan')
        post = Post.objects.create(
            author=author,
            text='Пост для подписки')
        response = (self.authorized_client2.
                    get(reverse('posts:follow_index')))

        self.assertNotIn(post, response.context['page_obj'])


class PaginatorViewsTest(BaseTest):
    def test_page_contains_correct_number_of_records(self):
        """Количество постов на первой странице равно 10, на второй 3."""
        pages = ['/', '/group/test-slug/', '/profile/Ivan/']
        for page in pages:
            with self.subTest(page=page):
                response = self.authorized_client.get(page)
                self.assertEqual(len(response.context['page_obj']), 10)
                response = self.authorized_client.get(page + '?page=2')
                self.assertEqual(len(response.context['page_obj']), 3)
