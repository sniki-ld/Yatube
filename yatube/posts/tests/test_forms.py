import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from ..models import Comment, Post
from ..tests.my_fixtures.posts_fixture import BaseTest

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class FormTests(BaseTest):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_new_post_create(self):
        """
        Валидная форма со страницы создания
        поста  создаёт новую запись в Post.
        """
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Создан новый пост',
        }

        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True)

        post_text_form = form_data['text']
        new_post = response.context['page_obj'][0].text
        self.assertRedirects(response, reverse(
            'posts:profile',
            kwargs={'username': 'Ivan'}))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(new_post, post_text_form)

    def test_edit_post(self):
        """
        Валидная форма со страницы редактирования поста
        изменяет пост с post_id.
        """
        posts_count = Post.objects.count()
        post_text = Post.objects.get(pk=1).text

        form_data = {
            'text': 'Текст после редактирования',
        }

        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': '1'}),
            data=form_data,
            follow=True)
        post_text_form = form_data['text']
        edit_post = Post.objects.get(pk=1).text

        self.assertEqual(Post.objects.count(), posts_count)
        self.assertRedirects(response, reverse(
            'posts:post_detail',
            kwargs={'post_id': '1'}))
        self.assertIsNot(post_text, edit_post)
        self.assertEqual(edit_post, post_text_form)

    def test_new_post_with_picture_create(self):
        """
        Валидная форма со страницы создания поста
        создаёт новую запись с картинкой.
        """
        posts_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Создан новый пост',
            'image': uploaded,
        }

        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True)

        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': 'Ivan'}))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.filter(
            text='Создан новый пост', image='posts/small.gif').exists())

    def test_post_with_image_is_on_pages(self):
        """Пост с изображением есть на страницах."""
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        Post.objects.create(
            author=self.user,
            text='Пост с картинкой',
            group=self.group,
            image=uploaded
        )

        pages = ['/', '/group/test-slug/', '/profile/Ivan/']
        for page in pages:
            with self.subTest(page=page):
                response = self.authorized_client.get(page)
                post_with_image = response.context['page_obj'][0]
                self.assertTrue(post_with_image.image)
                self.assertIn(post_with_image, response.context['page_obj'])

    def test_new_comment_create(self):
        """
        Валидная форма со страницы posts:post_detail
        создаёт новый комментарий
        """
        comment_count = Comment.objects.count()
        form_data = {
            'text': 'Создан новый комментарий',
        }
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': '1'}),
            data=form_data,
            follow=True)

        comment_text_form = form_data['text']
        new_comment = response.context['comments'][0]
        new_comment_text = new_comment.text
        new_comment_author = new_comment.author
        self.assertRedirects(response,
                             reverse('posts:post_detail',
                                     kwargs={'post_id': '1'}))
        self.assertEqual(Comment.objects.count(), comment_count + 1)
        self.assertEqual(comment_text_form, new_comment_text)
        self.assertIn(new_comment, response.context['comments'])
        self.assertTrue(new_comment_author.is_authenticated)
