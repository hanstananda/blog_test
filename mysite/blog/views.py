from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Post

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        """Return the last five published post."""
        return Post.objects.order_by('-pub_date')[:5]