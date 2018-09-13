from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Post, Category, UserProfile, Comments, Likes
from django.db.models import CharField, Value
from .forms import NameForm
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.db.models import Count

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'items_list'

    def get_queryset(self):
        self.posts_liked = []
        self.posts = Post.objects.all().annotate(num_likes=Count('likes'))[:5]
        self.categories = Category.objects.all()[:5]
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
        self.categories = Category.objects.all()[:5]
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


def like(request):
    if request.method == 'POST' and request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blog:success'))
    else:
        return HttpResponseRedirect(reverse('blog:fail'))


def unlike(request):
    if request.method == 'POST'and request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blog:success'))
    else:
        return HttpResponseRedirect(reverse('blog:fail'))


def comment(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('blog:success'))
    else:
        return HttpResponseRedirect(reverse('blog:fail'))


def success(request):
    return render(request, 'blog/success.html')


def fail(request):
    return render(request, 'blog/fail.html')

# Get Query for Liked on a post Likes.objects.filter(liked_on=get_object_or_404(Post,post_title='Test'))
