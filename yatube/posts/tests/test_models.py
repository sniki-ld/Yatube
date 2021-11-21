from ..tests.my_fixtures.posts_fixture import BaseTest


class PostModelTest(BaseTest):
    def test_model_group_have_correct_object_names(self):
        """__str__  group - это строчка с содержимым group.title."""
        group = PostModelTest.group
        expected_object_name_group = group.title
        self.assertEqual(expected_object_name_group, str(group))

    def test_model_post_have_correct_object_names(self):
        """__str__  post - это строчка с содержимым post.text."""
        post = PostModelTest.post
        expected_object_name_post = post.text[:15]
        self.assertEqual(expected_object_name_post, str(post))

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Выберите группу',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value)
