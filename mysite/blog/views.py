from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Post, Category
from django.db.models import CharField, Value
from .forms import NameForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse

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

    def __init__(self):
        self.category = None

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

    @login_required()
    def show_user(self):
        pass



def login(request):
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
                return HttpResponseRedirect(reverse('blog:success'))
        return HttpResponseRedirect(reverse('blog:fail'))

    else:
        return HttpResponseRedirect(reverse('blog:fail'))


def success(request):
    return render(request, 'blog/success.html')


def fail(request):
    return render(request, 'blog/fail.html')
