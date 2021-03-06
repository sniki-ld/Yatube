from http import HTTPStatus

from posts.tests.my_fixtures.posts_fixture import BaseTest


class PostURLTests(BaseTest):
    def test_create_page_anonymous(self):
        """Страница /auth/signup/ доступна любому пользователю."""
        response = self.guest_client.get('/auth/signup/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_url_authorized(self):
        """Страницы доступны авторизованному пользователю."""
        pages = ['/auth/logout/', '/auth/login/',
                 '/auth/password_reset/', '/auth/password_reset/done/',
                 '/auth/reset/<uidb64>/<token>/', '/auth/reset/done/']
        for page in pages:
            with self.subTest(page=page):
                response = self.authorized_client.get(page)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_password_change_page_anonymous(self):
        """
        Страница /auth/password_change/
        перенаправляет анонимного пользователя.
        """
        response = self.guest_client.get('/auth/password_change/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/auth/password_change/')

    def test_password_change_done_page_anonymous(self):
        """
        Страница /auth/password-change/done/
        перенаправляет анонимного пользователя.
        """
        response = self.guest_client.get('/auth/password-change/done/',
                                         follow=True)
        self.assertRedirects(
            response,
            '/auth/login/?next=/auth/password-change/done/')
