from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post, User

POST_PER_PAGE = 10


def index(request):
    title = 'Последние обновления на сайте'
    post_list = Post.objects.all()
    paginator = Paginator(post_list, POST_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': title,
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    title = 'Записи сообщества'
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, POST_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': title,
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    title = 'Профайл пользователя'
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    paginator = Paginator(post_list, POST_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = author.posts.count()
    following = None
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user, author=author).exists()
    context = {
        'title': title,
        'author': author,
        'page_obj': page_obj,
        'count': count,
        'following': following
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    title = 'Полный текст поста'
    post = get_object_or_404(Post, pk=post_id)
    count = post.author.posts.count()
    form = CommentForm()
    comment = Comment.objects.filter(post=post_id)

    context = {
        'title': title,
        'post': post,
        'count': count,
        'form': form,
        'comments': comment
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=post.author.username)
        return render(request, 'posts/post_create.html', {'form': form})

    return render(request, 'posts/post_create.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None,
                    files=request.FILES or None, instance=post)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post.pk)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id=post.pk)

    context = {
        'form': form,
        'post_id': post.pk
    }
    return render(request, 'posts/post_create.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

        return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    title = 'Ваши подписки'
    post_list_follow = Post.objects.filter(
        author__following__user=request.user)
    paginator = Paginator(post_list_follow, POST_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': title,
        'page_obj': page_obj,
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if Follow.objects.filter(
            user=request.user,
            author=author).exists() or request.user == author:
        return redirect('posts:index')
    Follow.objects.create(user=request.user, author=author)

    return redirect('posts:follow_index')


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    unfollow = Follow.objects.get(user=request.user, author=author)
    unfollow.delete()

    return redirect('posts:index')
