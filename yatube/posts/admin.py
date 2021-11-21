from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse

from .models import Group, Post, Comment
from .parsers import xlsx_group_parser


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'description',)
    search_fields = ('title', 'description',)
    prepopulated_fields = {'slug': ('title',)}
    empty_value_display = '-пусто-'
    change_list_template = 'admin/group_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('group-updating/',
                 self.admin_site.admin_view(self.group_updating),
                 name='group-updating')
        ]
        return my_urls + urls

    def group_updating(self, request):
        """group updating for exel file"""
        redirect_url = reverse('admin:posts_group_changelist')
        if request.method != 'POST':
            self.message_user(request, 'Не выбран файл', messages.ERROR)
            return HttpResponseRedirect(redirect_url)
        file = request.FILES['file']

        groups = xlsx_group_parser.xlsx_group_parser(file)
        try:
            Group.objects.bulk_create(groups)
        except Exception as e:
            self.message_user(
                request, f'Ошибка добавления групп: {e}', messages.ERROR)
            return HttpResponseRedirect(redirect_url)
        self.message_user(
            request, f'{"Группы добавлены"}', messages.SUCCESS)
        return HttpResponseRedirect(redirect_url)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'created',
        'author',
        'post',
    )
    list_editable = ('post',)
    search_fields = ('text',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
