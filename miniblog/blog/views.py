from django.shortcuts import get_object_or_404, render
from blog.models import Blogpost, Comments, Author
from django.views import generic
from django.views.generic.edit import FormMixin
from django.urls import reverse
from blog.forms import CreateComments


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


class BlogDetailView(FormMixin, generic.DetailView):
    model = Blogpost
    slug_field = 'id'
    slug_url_kwarg = 'id'
    form_class = CreateComments

    def get_success_url(self):
        return reverse('blogpost-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context['form'] = CreateComments()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog_post = get_object_or_404(Blogpost, pk=self.kwargs['pk'])
        form.save()
        return super(BlogDetailView, self).form_valid(form)
