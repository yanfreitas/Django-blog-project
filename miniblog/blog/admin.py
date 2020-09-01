from django.contrib import admin
from blog.models import Post, Comment


class CommentsInline(admin.TabularInline):
    """Insert the comments in the post page on the admin page"""
    model = Comment
    extra = False


@admin.register(Post)
class BlogpostAdmin(admin.ModelAdmin):
    """Register the posts model on the admin page"""
    list_display = ('title', 'date', 'author')
    list_filter = ('date',)
    inlines = [CommentsInline]


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    """Register the comments model on the admin page"""
    list_display = ('author', 'blog_post', 'date_time')
    list_filter = ('date_time',)
