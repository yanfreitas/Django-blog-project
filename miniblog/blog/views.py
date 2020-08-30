from django.shortcuts import get_object_or_404
from blog.models import Post, Comments
from django.views import generic
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from blog.forms import CreateComments
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


class PostListView(generic.ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 5


class UserPostListView(generic.ListView):
    model = Post
    template_name = 'blog/user_post.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date')


class PostDetailView(FormMixin, generic.DetailView):
    model = Post
    form_class = CreateComments

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        actual_post = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if actual_post.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['total_likes'] = actual_post.total_likes()
        context['liked'] = liked
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
        form.instance.blog_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.save()
        return super(PostDetailView, self).form_valid(form)


def LikeView(request, pk):

    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_success_url(self):
        return reverse('index')


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Comments

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author or self.request.user == comment.blog_post.author:
            return True
        return False

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.get_object().blog_post.id})
