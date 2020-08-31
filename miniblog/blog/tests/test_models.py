from django.test import TestCase
from blog.models import Posts, Comments
from django.contrib.auth.models import User
from .base_tests import test_model_fields_label, test_model_fields_max_length


class PostAuthorTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create an user
        test_user = User.objects.create_user(username='user1', password='user1senha')
        test_user2 = User.objects.create_user(username='user2', password='user2senha')
        test_user.save()
        test_user2.save()

        # create a post
        post = Posts.objects.create(title='testpost', author=test_user)
        post.likes.add(test_user)
        post.likes.add(test_user2)

    def test_title_label(self):
        test_model_fields_label(self, Posts, 'title', 'title')

    def test_description_label(self):
        test_model_fields_label(self, Posts, 'description', 'description')

    def test_date_label(self):
        test_model_fields_label(self, Posts, 'date', 'date')

    def test_author_label(self):
        test_model_fields_label(self, Posts, 'author', 'author')

    def test_likes_label(self):
        test_model_fields_label(self, Posts, 'likes', 'likes')

    def test_title_max_length(self):
        test_model_fields_max_length(self, Posts, 'title', 200)

    def test_description_max_length(self):
        test_model_fields_max_length(self, Posts, 'description', 1000)

    def test_total_likes(self):
        post = Posts.objects.get(id=1)
        expected_total_likes = 2
        self.assertEquals(expected_total_likes, post.total_likes())

    def test_object_name(self):
        post = Posts.objects.get(id=1)
        expected_name = post.title
        self.assertEquals(expected_name, str(post))

    def test_get_absolute_url(self):
        post = Posts.objects.get(id=1)
        self.assertEquals(post.get_absolute_url(), '/blog/post/1/')


class CommentsAuthorTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create an user
        test_user = User.objects.create_user(username='user1', password='user1senha')
        test_user.save()

        # create a post
        post = Posts.objects.create(title='testpost', author=test_user)

        # create a coment
        Comments.objects.create(author=test_user, blog_post=post)

    def test_description_label(self):
        test_model_fields_label(self, Comments, 'description', 'description')

    def test_date_time_label(self):
        test_model_fields_label(self, Comments, 'date_time', 'date time')

    def test_blog_post_label(self):
        test_model_fields_label(self, Comments, 'blog-post', 'blog post')

    def test_author_label(self):
        test_model_fields_label(self, Comments, 'author', 'author')

    def test_description_max_length(self):
        test_model_fields_max_length(self, Comments, 'description', 300)
