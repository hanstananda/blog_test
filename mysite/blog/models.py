from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

    class Meta:
        ordering = ["-category_name"]


class UserProfile(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_image = models.ImageField(default=None, blank=True, null=True)

    def __str__(self):
        return self.user_name.username


class Post(models.Model):
    post_title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    post_content = models.TextField(max_length=100000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.post_title


class Likes(models.Model):
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_on = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.liked_by+self.liked_on

    class Meta:
        unique_together = ('liked_by', 'liked_on')


class Comments(models.Model):
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    commented_on = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.commented_by+self.commented_on
