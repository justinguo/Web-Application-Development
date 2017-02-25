from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)
    email = models.EmailField(blank=True)
    img = models.ImageField(upload_to="user_pics", blank=True, default='user_pics/user_default.png')
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    self_description = models.CharField(max_length=400, blank=True)
    followers = models.ManyToManyField('self', blank=True,
                                       related_name='following', symmetrical=False)

    def __unicode__(self):
        return self.user.username


class Post(models.Model):
    profile = models.ForeignKey(Profile, related_name="post_profile")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="post_pics", blank=True, null=True)
    textpost = models.CharField(max_length=400)
    message = models.ManyToManyField(Profile, blank=True, default="",
      symmetrical=False)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.profile.user.username

    @staticmethod
    def get_all_posts():
        return Post.objects.all()

    class Meta:
        ordering = ('-id',)


class Comment(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL, related_name="comments")
    profile = models.ForeignKey(Profile)
    comment = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.profile.user.username

    @staticmethod
    def get_comments(post):
        return Comment.objects.filter(post=post)
