from django import forms
from django.forms import HiddenInput, Select
from .models import Post, Category, UserProfile, Comments, Likes


class NameForm(forms.Form):
    username = forms.CharField(label='Username', max_length=25)
    password = forms.CharField(label='Password', max_length=25)


class CategoryForm(forms.Form):
    class Meta:
        model = Category
    name = forms.CharField(label='category', max_length=100)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'post_title', 'post_content', 'pub_date']
        widgets = {
            'pub_date': HiddenInput(),
            'category': Select(attrs={'class': 'ui search dropdown'})

        }

