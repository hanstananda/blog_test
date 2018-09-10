from django.db import models

# Create your models here.


class Post(models.Model):
    post_title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    post_content = models.CharField(max_length=100000)

    def __str__(self):
        return self.post_title
