from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Post, Category, UserProfile, Comments, Likes
from django.db.models import CharField, Value
from .forms import NameForm, EditCategoryForm
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.template import Template
from django.http import HttpResponse

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'items_list'

    def get_queryset(self):
        self.posts_liked = []
        self.posts = Post.objects.all().annotate(num_likes=Count('likes'))[:5]
        self.categories = Category.objects.all()
        if self.request.user.is_authenticated:
            self.user_profile = get_object_or_404(UserProfile, user_name=self.request.user)
            for item in self.posts:
                temp = item.likes_set.values().filter(liked_on_id=item.id, liked_by=self.request.user.id).count()
                if temp > 0:
                    self.posts_liked += list([item.post_title])
        else:
            self.user_profile = None
        all_items = []
        return all_items

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the category
        context['user_profile'] = self.user_profile
        context['posts'] = self.posts
        context['posts_liked'] = self.posts_liked
        context['categories'] = self.categories
        return context


class CategoryPostList(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'items_list'

    def __init__(self):
        self.user_profile = None

    def get_queryset(self):
        self.posts_liked = []
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        self.posts = Post.objects.filter(category=self.category)[:5]
        self.categories = Category.objects.all()
        self.likes =Likes.objects.all()
        if self.request.user.is_authenticated:
            self.user_profile = get_object_or_404(UserProfile, user_name=self.request.user)
            for item in self.posts:
                temp = item.likes_set.values().filter(liked_on_id=item.id, liked_by=self.request.user.id).count()
                if temp > 0:
                    self.posts_liked += list([item.post_title])
        else:
            self.user_profile = None
        all_items = []
        return all_items

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the category
        context['category'] = self.category
        context['user_profile'] = self.user_profile
        context['posts'] = self.posts
        context['posts_liked'] = self.posts_liked
        context['categories'] = self.categories
        return context


class PostView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'items_list'

    def __init__(self):
        self.user_profile = None

    def get_queryset(self):
        self.posts_liked = []
        self.posts = Post.objects.filter(pk=self.kwargs['pk'])
        self.post=get_object_or_404(Post, pk=self.kwargs['pk'])
        self.users_profile = UserProfile.objects.all()
        self.category = get_object_or_404(Category, pk=self.post.category.id)
        self.categories = Category.objects.all().filter()
        self.comments = Comments.objects.filter(commented_on=self.post)
        self.likes = Likes.objects.all()
        if self.request.user.is_authenticated:
            self.user_profile = get_object_or_404(UserProfile, user_name=self.request.user)
            for item in self.posts:
                temp = item.likes_set.values().filter(liked_on_id=item.id, liked_by=self.request.user.id).count()
                if temp > 0:
                    self.posts_liked += list([item.post_title])
        else:
            self.user_profile = None
        all_items = []
        return all_items

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the category
        context['user_profile'] = self.user_profile
        context['posts'] = self.posts
        context['post'] = self.post
        context['posts_liked'] = self.posts_liked
        context['categories'] = self.categories
        context['category'] = self.category
        context['comments'] = self.comments
        context['users_profile'] = self.users_profile
        return context


def admin_view(request):
    if request.user.is_authenticated:
        return render(request, 'blog/admin.html')
    else:
        return HttpResponseRedirect(reverse('blog:fail'))


class PostsAdminView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'blog/admin_posts.html'

    def get_context_data(self, **kwargs):
        self.posts = Post.objects.all().annotate(num_comments=Count('comments'))
        context = super().get_context_data(**kwargs)
        context['posts'] = self.posts
        return context


class PostsAdminCreate(LoginRequiredMixin, generic.TemplateView):
    template_name = 'blog/admin_posts_create.html'


class PostsAdminEdit(LoginRequiredMixin, generic.TemplateView):
    template_name = 'blog/admin_posts_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_id'] = self.kwargs['pk']
        return context


def add_post(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            post_name = request.POST.get('post_name', '')
            pub_date = datetime.now()
            category_from_request = Category(category_name=category_name, pub_date=pub_date)
            category_from_request.save()
        except:
            return HttpResponseRedirect(reverse('blog:fail'))
        return HttpResponseRedirect(reverse('blog:success'))
    else:
        return HttpResponseRedirect(reverse('blog:fail'))


class CategoriesAdminView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'blog/admin_categories.html'

    def get_context_data(self, **kwargs):
        self.categories = Category.objects.all().annotate(num_posts=Count('post'))[:5]
        context = super().get_context_data(**kwargs)
        context['categories'] = self.categories
        return context


class CategoriesAdminCreate(LoginRequiredMixin, generic.TemplateView):
    template_name = 'blog/admin_categories_create.html'


class CategoriesAdminEdit(LoginRequiredMixin, generic.TemplateView):
    template_name = 'blog/admin_categories_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs['pk']
        return context


def add_category(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            category_name = request.POST.get('category', '')
            pub_date = datetime.now()
            category_from_request = Category(category_name=category_name, pub_date=pub_date)
            category_from_request.save()
        except:
            return HttpResponseRedirect(reverse('blog:fail'))
        return HttpResponseRedirect(reverse('blog:success'))
    else:
        return HttpResponseRedirect(reverse('blog:fail'))


def delete_category(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            category_id = request.POST.get('category_id', '')
            category_from_request = Category.objects.filter(id=category_id)
            category_from_request.delete()
        except:
            return HttpResponseRedirect(reverse('blog:fail'))
        return HttpResponseRedirect(reverse('blog:success'))
    else:
        return HttpResponseRedirect(reverse('blog:fail'))


def edit_category(request):
    if request.method == 'POST' and request.user.is_authenticated:
        # form = EditCategoryForm(request.POST)
        # check whether it's valid:
        # if form.is_valid():
        # category_name = form.cleaned_data['category_name']
        # category_id = form.cleaned_data['category_id']
        category_name = request.POST.get('category')
        category_id = request.POST.get('category_id')
        category_from_request = get_object_or_404(Category, id=category_id)
        category_from_request.category_name = category_name
        category_from_request.save()
        return HttpResponseRedirect(reverse('blog:success'))
        # return HttpResponseRedirect(reverse('blog:fail'))
    else:
        return HttpResponseRedirect(reverse('blog:fail'))


class UsersAdminView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'blog/admin_users.html'

    def get_context_data(self, **kwargs):
        self.users_profiles = UserProfile.objects.all()
        self.users= []
        for user in self.users_profiles:
            num_post = Comments.objects.all().filter(commented_by=user.user_name).count()
            user_changed = {
                'user_name': user.user_name,
                'join_date': user.join_date,
                'matric_number': user.matric_number,
                'num_posts': num_post,
                'is_not_banned': user.user_name.is_active,
            }
            # user_changed = UserProfile.objects.all().filter(
            #    user_name=user.user_name).annotate(num_posts=Value(num_post))
            #  use Value() to pass the number directly
            self.users.append(user_changed)

        context = super().get_context_data(**kwargs)
        context['users'] = self.users
        return context


def ban_user(request):
    if request.method == 'POST' and request.user.is_authenticated:
        user_id = request.POST.get('user_id')
        user_from_request = get_object_or_404(User, id=user_id)
        user_from_request.is_active = False
        user_from_request.save()
        return HttpResponseRedirect(reverse('blog:success'))
    else:
        return HttpResponseRedirect(reverse('blog:fail'))


def unban_user(request):
    if request.method == 'POST' and request.user.is_authenticated:
        user_id = request.POST.get('user_id')
        user_from_request = get_object_or_404(User, id=user_id)
        user_from_request.is_active = True
        user_from_request.save()
        return HttpResponseRedirect(reverse('blog:success'))
    else:
        return HttpResponseRedirect(reverse('blog:fail'))


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect(reverse('blog:success'))
    return HttpResponseRedirect(reverse('blog:fail'))


def login_view(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('blog:success'))
        return HttpResponseRedirect(reverse('blog:fail'))

    else:
        return HttpResponseRedirect(reverse('blog:fail'))


def add_comment(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            post_id = request.POST.get('post_id', '')
            user_id = request.POST.get('user_id', '')
            comment_text = request.POST.get('comment', '')
            if(len(comment_text)<10):
                raise ModuleNotFoundError
            like_from_request = Comments(commented_on=get_object_or_404(Post, id=post_id),
                                      commented_by=get_object_or_404(User, id=user_id),
                                      comment_content=comment_text,
                                      )
            like_from_request.save()
        except:
            return HttpResponseRedirect(reverse('blog:fail'))
        return HttpResponseRedirect(reverse('blog:success'))
    else:
        return HttpResponseRedirect(reverse('blog:fail'))


def like(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            post_id = request.POST.get('post_id', '')
            user_id = request.POST.get('user_id', '')
            like_from_request = Likes(liked_on=get_object_or_404(Post, id=post_id),
                                      liked_by=get_object_or_404(User, id=user_id))
            like_from_request.save()
            # Note: No checking between user_id sent and user authenticated yet
        except:
            return HttpResponseRedirect(reverse('blog:fail'))
        return HttpResponseRedirect(reverse('blog:success'))
    else:
        return HttpResponseRedirect(reverse('blog:fail'))


def unlike(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            like_from_request = Likes.objects.filter(liked_on=request.POST.get('post_id', ''),
                                                     liked_by=request.POST.get('user_id', ''))
            if like_from_request.count() > 0:
                like_from_request.delete()
            else:
                raise ModuleNotFoundError
        except:
            return HttpResponseRedirect(reverse('blog:fail'))
        return HttpResponseRedirect(reverse('blog:success'))
    else:
        return HttpResponseRedirect(reverse('blog:fail'))


"""def comment(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('blog:success'))
    else:
        return HttpResponseRedirect(reverse('blog:fail'))"""


def success(request):
    return render(request, 'blog/success.html')


def fail(request):
    return render(request, 'blog/fail.html')


# Get Query for Liked on a post Likes.objects.filter(liked_on=get_object_or_404(Post,post_title='Test'))
