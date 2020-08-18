from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Blogpost(models.Model):

    """Model representing a blog post"""
    title = models.CharField(max_length=200, help_text='Enter a post title')
    date = models.DateField(auto_now_add=True)
    description = models.TextField(max_length=1000, help_text='Enter a description for the post')

    # Foreign Key used because post can only have one author, but authors can have multiple posts
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object"""
        return self.title

    def get_absolute_url(self):
        """Returns the url to acces a detail record for this book"""
        return reverse('blogpost-detail', args=[str(self.id)])

    class Meta:
        ordering = ['-date']


class Author(models.Model):
    """Model for representing an author of a post"""
    username = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField(max_length=1000, help_text='Enter the biography for the user')

    def __str__(self):
        """String for representing the Model object"""
        return str(self.username)

    def get_absolute_url(self):
        """Returns the url to access a particular author instance"""
        return reverse('author-detail', args=[str(self.id)])


class Comments(models.Model):
    """Model for representing a comment on the post"""
    description = models.TextField(max_length=300, help_text='Enter a comment to the post')
    date_time = models.DateTimeField(auto_now_add=True)

    blog_post = models.ForeignKey(Blogpost, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['date_time']

