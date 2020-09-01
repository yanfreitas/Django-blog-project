from django.test import TestCase
from blog.models import Post, Comment
from django.contrib.auth.models import User


class PostAuthorTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create an user
        test_user = User.objects.create_user(username='user1', password='user1senha')
        test_user2 = User.objects.create_user(username='user2', password='user2senha')
        test_user.save()
        test_user2.save()

        # create a post
        post = Post.objects.create(title='testpost', author=test_user)
        post.likes.add(test_user)
        post.likes.add(test_user2)

    def test_title_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_description_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_date_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('date').verbose_name
        self.assertEquals(field_label, 'date')

    def test_author_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'author')

    def test_likes_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('likes').verbose_name
        self.assertEquals(field_label, 'likes')

    def test_title_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)

    def test_description_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('description').max_length
        self.assertEquals(max_length, 1000)

    def test_total_likes(self):
        post = Post.objects.get(id=1)
        expected_total_likes = 2
        self.assertEquals(expected_total_likes, post.total_likes())

    def test_object_name(self):
        post = Post.objects.get(id=1)
        expected_name = post.title
        self.assertEquals(expected_name, str(post))

    def test_get_absolute_url(self):
        post = Post.objects.get(id=1)
        self.assertEquals(post.get_absolute_url(), '/blog/post/1/')


class CommentsAuthorTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create an user
        test_user = User.objects.create_user(username='user1', password='user1senha')
        test_user.save()

        # create a post
        post = Post.objects.create(title='testpost', author=test_user)

        # create a coment
        Comment.objects.create(author=test_user, blog_post=post)

    def test_description_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_date_time_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('date_time').verbose_name
        self.assertEquals(field_label, 'date time')

    def test_blog_post_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('blog_post').verbose_name
        self.assertEquals(field_label, 'blog post')

    def test_author_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'author')

    def test_description_max_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field('description').max_length
        self.assertEquals(max_length, 300)
