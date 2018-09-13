from django.contrib import admin
from .models import Post, Category, UserProfile, Likes, Comments

# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Likes)
admin.site.register(Comments)
