from django.db import models

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

    class Meta:
        ordering = ["-category_name"]


class User(models.Model):
    user_name = models.CharField(max_length=25)


class Post(models.Model):
    post_title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    post_content = models.CharField(max_length=100000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    User = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.post_title


