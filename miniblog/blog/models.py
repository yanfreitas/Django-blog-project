from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):

    """Model representing a blog post"""
    title = models.CharField(max_length=200, help_text='Enter a post title')
    description = models.TextField(max_length=1000, help_text='Enter a description for the post')
    date = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='blog_post')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        """String for representing the Model object"""
        return self.title

    def get_absolute_url(self):
        """Returns the url to acces a detail record for this book"""
        return reverse('post-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-date']


class Comments(models.Model):
    """Model for representing a comment on the post"""
    description = models.TextField(max_length=300)
    date_time = models.DateTimeField(default=timezone.now)

    blog_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date_time']
