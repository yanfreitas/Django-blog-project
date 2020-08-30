from django.contrib import admin
from blog.models import Posts, Comments


class CommentsInline(admin.TabularInline):
    """Insert the comments in the post page on the admin page"""
    model = Comments
    extra = False


@admin.register(Posts)
class BlogpostAdmin(admin.ModelAdmin):
    """Register the posts model on the admin page"""
    list_display = ('title', 'date', 'author')
    list_filter = ('date',)
    inlines = [CommentsInline]


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    """Register the comments model on the admin page"""
    list_display = ('author', 'blog_post', 'date_time')
    list_filter = ('date_time',)
