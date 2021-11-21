from http import HTTPStatus

from ..tests.my_fixtures.posts_fixture import BaseTest


class PostURLTests(BaseTest):
    def test_pages_url_anonymous(self):
        """Страницы доступны любому пользователю."""
        pages = ['/', '/group/test-slug/', '/profile/Ivan/', '/posts/1/']
        for page in pages:
            with self.subTest(page=page):
                response = self.guest_client.get(page)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_url_authorized(self):
        """Страницы доступны авторизованному пользователю."""
        pages = ['/', '/group/test-slug/',
                 '/profile/Ivan/', '/posts/1/', '/create/']
        for page in pages:
            with self.subTest(page=page):
                response = self.authorized_client.get(page)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_page_anonymous(self):
        """Страница /create/ перенаправляет анонимного пользователя."""
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/create/')

    def test_post_edit_page_anonymous(self):
        """
        Страница posts/<post_id>/edit/
        перенаправляет анонимного пользователя.
        """
        response = self.guest_client.get('/posts/1/edit/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/posts/1/edit/')

    def test_nonexistent_page_any_user(self):
        """
        Запрос любого пользователя к несуществующей
        странице возвращает ошибку 404.
        """
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        response = self.authorized_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_post_edit_page_author(self):
        """
        Страница posts/<post_id>/edit/
        перенаправляет авторизованного пользователя.
        """
        response = self.authorized_client2.get('/posts/1/edit/')
        self.assertRedirects(response, '/posts/1/')

    def test_post_edit_page_no_author(self):
        """Страница posts/<post_id>/edit/ доступна только автору поста."""
        if self.user == self.post.author:
            response = self.authorized_client.get('/posts/1/edit/')
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        pages_templates = {
            '/': 'posts/index.html',
            '/group/test-slug/': 'posts/group_list.html',
            '/profile/Ivan/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
            '/create/': 'posts/post_create.html',
            '/posts/1/edit/': 'posts/post_create.html',
            '/unexisting_page/': 'core/404.html'
        }
        for page, template in pages_templates.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(page)
                self.assertTemplateUsed(response, template)
