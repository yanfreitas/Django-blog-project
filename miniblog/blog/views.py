from django.shortcuts import get_object_or_404, render, get_list_or_404
from blog.models import Blogpost, Comments, Author
from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.http import HttpResponseRedirect


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


class BlogDetailView(generic.DetailView):
    model = Blogpost
    slug_field = 'id'
    slug_url_kwarg = 'id'


class CommentsCreate(CreateView):
    model = Comments
    fields = ('description',)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog_post = get_object_or_404(Blogpost, pk=self.kwargs['pk'])
        return super(CommentsCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('blogpost-detail', kwargs={'id': self.kwargs['pk'],})

    def get_context_data(self, **kwargs):
        context = super(CommentsCreate, self).get_context_data(**kwargs)
        context['blog_post'] = get_object_or_404(Blogpost, pk=self.kwargs['pk'])
        return context
