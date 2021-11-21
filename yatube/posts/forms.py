from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {
            'text': _('Текст Поста'), 'group': _('Группа Поста'),
        }
        help_texts = {
            'text': _(' Текст нового Поста'),
            'group': _('Группа, к которой будет относиться Пост'),

        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': _('Текст Комментария'), 'author': _('Автор Комментария'),
        }
        help_texts = {
            'text': _(' Текст нового Комментария'),
            'author': _('Автор написавший комментарий'),
        }
