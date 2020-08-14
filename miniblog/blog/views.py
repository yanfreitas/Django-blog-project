from django.shortcuts import render
from blog.models import Blogpost, Comments


def index(request):
    """View function for home page of site"""

    posts = Blogpost.objects.filter().order_by('-date')

    context = {
        'posts': posts,
    }

    return render(request, 'index.html', context=context)