from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Post, Category
from django.db.models import CharField, Value
from .forms import NameForm

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'items_list'

    def get_queryset(self):
        """Return the last five published post."""
        posts = Post.objects.annotate(type=Value('post', CharField()))
        categories = Category.objects.annotate(type=Value('category', CharField()))
        all_items = list(posts) + list(categories)
        return all_items


class CategoryPostList(generic.ListView):

    template_name = 'blog/index.html'
    context_object_name = 'items_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        posts = Post.objects.filter(category=self.category)
        posts = posts.annotate(type=Value('post', CharField()))
        categories = Category.objects.annotate(type=Value('category', CharField()))
        all_items = list(posts) + list(categories)
        return all_items

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the category
        context['category'] = self.category
        return context


