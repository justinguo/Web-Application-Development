from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=160)
    post_time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def display_post(user):
        return Post.objects.filter(author=user).order_by("-post_time")

    def __unicode__(self):
        return self.title