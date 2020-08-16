from django.shortcuts import render
from blog.models import Blogpost, Comments, Author
from django.views import generic


def index(request):
    """View function for home page of site"""

    posts = Blogpost.objects.filter()

    context = {
        'posts': posts,
    }

    return render(request, 'index.html', context=context)


class BlogListView(generic.ListView):
    model = Blogpost
    paginate_by = 5


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author
    slug_field = 'id'
    slug_url_kwarg = 'id'

