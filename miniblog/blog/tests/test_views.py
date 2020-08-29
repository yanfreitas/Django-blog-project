from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.utils import timezone

from blog.models import Post, Comments
from blog.forms import CreateComments
from blog.views import LikeView
import pdb


class PostListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create users
        test_user = User.objects.create_user(username='user1', password='user1senha')
        test_user.save()

        # creats posts
        posts = 13

        for post_id in range(posts):
            Post.objects.create(
                title=f'post {post_id}',
                author=test_user
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/')
        self.assertEquals(response.status_code, 200)

    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_pagination_is_five(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['posts']) == 5)

    def test_lists_all_posts(self):
        response = self.client.get(reverse('index') + '?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(len(response.context['posts']) == 3)


class UserPostListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create users
        test_user = User.objects.create_user(username='user1', password='user1senha')
        test_user2 = User.objects.create_user(username='user2', password='user2senha')
        test_user.save()
        test_user2.save()

        # creats posts
        posts = 13

        for post_id in range(posts):
            if post_id % 2 == 0:
                Post.objects.create(
                    title=f'post {post_id}',
                    author=test_user,
                    description='some description'
                )
            Post.objects.create(
                title=f'post {post_id}',
                author=test_user2,
                description='some description'
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/user/user1/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('user-post', kwargs={'username': 'user1'}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('user-post', kwargs={'username': 'user1'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/user_post.html')

    def test_pagination_is_five(self):
        response = self.client.get(reverse('user-post', kwargs={'username': 'user1'}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['posts']) == 5)

    def test_lists_all_posts(self):
        # Get second page and confirm it has (exactly) remaining 2 items
        response = self.client.get(reverse('user-post', kwargs={'username': 'user1'}) + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['posts']) == 2)

    def test_get_queryset(self):
        response = self.client.get(reverse('user-post', kwargs={'username': 'user1'}))
        self.assertEqual(response.status_code, 200)
        for post in response.context['posts']:
            self.assertEqual(post.author.username, 'user1')


class PostDetailViewTest(TestCase):

    def setUp(self):
        # create users
        test_user = User.objects.create_user(username='user1', password='user1senha')
        test_user.save()

        # creats posts
        posts = 2

        for post_id in range(posts):
            Post.objects.create(
                title=f'post {post_id}',
                author=test_user
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/post/1/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('post-detail', kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('post-detail', kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_redirects_to_correct_page_if_commented(self):
        login = self.client.login(username='user1', password='user1senha')
        response = self.client.post(reverse('post-detail', kwargs={'pk': '1'}), {'description': 'test'})
        print(type(response))
        post = Post.objects.get(id=1)
        comments = post.comments_set.all()
        self.assertRedirects(response, reverse('post-detail', kwargs={'pk': '1'}))
        self.assertEqual(len(comments), 1)


class LikeViewTest(TestCase):

    def setUp(self):

        # create users
        test_user = User.objects.create_user(username='user1', password='user1senha')
        test_user.save()

        # creats posts

        Post.objects.create(
            title='post 1',
            author=test_user
        )

    def test_likes(self):
        login = self.client.login(username='user1', password='user1senha')
        p = self.client.get(reverse('post-detail', kwargs={'pk': '1'}))
        response = self.client.post(reverse('post-detail', kwargs={'pk': '1'}), {'post_id': True})
        p = self.client.get(reverse('post-detail', kwargs={'pk': '1'}))
        # print(response)
        self.assertEqual(p.context['total_likes'], 1)
        self.assertRedirects(response, reverse('post-detail', kwargs={'pk': '1'}))

    #def test_likes_redirects_to_correct_template(self):
     #   login = self.client.login(username='user1', password='user1senha')
      #  post = self.client.get(reverse('post-detail', kwargs={'pk': '1'}))
       # response = self.client.post(reverse('post-detail', kwargs={'pk': '1'}), post.context['object'].likes.add(post.context['user']))
        #print(2response)
        #self.assertRedirects(response, reverse('post-detail', kwargs={'pk': '1'}))


class PostCreateViewTest(TestCase):

    def setUp(self):
        # create users
        test_user = User.objects.create_user(username='user1', password='user1senha')
        test_user.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response, '/login/?next=/blog/post/new/')

    def test_redirect_if_logged_in(self):
        login = self.client.login(username='user1', password='user1senha')
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(username='user1', password='user1senha')
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'blog/post_form.html')

    def test_title_is_invalid(self):
        login = self.client.login(username='user1', password='user1senha')
        response = self.client.post(reverse('post-create'), {'title': '', 'description': 'test'})
        self.assertEqual(response.status_code, 200)

    def test_description_is_invalid(self):
        login = self.client.login(username='user1', password='user1senha')
        response = self.client.post(reverse('post-create'), {'title': 'test', 'description': ''})
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_form_is_valid(self):
        login = self.client.login(username='user1', password='user1senha')
        response = self.client.post(reverse('post-create'), {'title': 'test', 'description': 'test'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/blog/post/'))

        # checking if the post was created.
        post = Post.objects.get(id=1)
        self.assertTrue(post)


class PostUpdateViewTest(TestCase):

    def setUp(self):
        # create users
        test_user = User.objects.create_user(username='user1', password='user1senha')
        test_user2 = User.objects.create_user(username='user2', password='user2senha')
        test_user2.save()
        test_user.save()

        # creats posts

        Post.objects.create(
            title=f'post {1}',
            author=test_user
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('post-update', kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/blog/post/1/update/')

    def test_redirect_if_logged_in_but_not_author_of_post(self):
        login = self.client.login(username='user2', password='user2senha')
        response = self.client.get(reverse('post-update', kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_and_author_of_post(self):
        login = self.client.login(username='user1', password='user1senha')
        response = self.client.get(reverse('post-update', kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(username='user1', password='user1senha')
        response = self.client.get(reverse('post-update', kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'blog/post_form.html')

    def test_title_is_invalid(self):
        login = self.client.login(username='user1', password='user1senha')
        response = self.client.post(reverse('post-update', kwargs={'pk': '1'}), {'title': '', 'description': 'test'})
        self.assertEqual(response.status_code, 200)

    def test_description_is_invalid(self):
        login = self.client.login(username='user1', password='user1senha')
        response = self.client.post(reverse('post-update', kwargs={'pk': '1'}), {'title': 'test', 'description': ''})
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_form_is_valid(self):
        login = self.client.login(username='user1', password='user1senha')
        response = self.client.post(reverse('post-update', kwargs={'pk': '1'}), {'title': 'test', 'description': 'test'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/blog/post/'))

        # checking if the post was created.
        post = Post.objects.get(id=1)
        self.assertTrue(post)


class PostDeleteViewTest(TestCase):

    def setUp(self):
        # create users
        test_user = User.objects.create_user(username='user1', password='user1senha')
        test_user2 = User.objects.create_user(username='user2', password='user2senha')
        test_user2.save()
        test_user.save()

        # creats post

        self.post = Post.objects.create(
            title=f'post {1}',
            author=test_user
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/blog/post/1/delete/')

    def test_redirect_if_logged_in_but_not_author_of_post(self):
        login = self.client.login(username='user2', password='user2senha')
        response = self.client.get(reverse('post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_and_author_of_post(self):
        login = self.client.login(username='user1', password='user1senha')
        response = self.client.get(reverse('post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(username='user1', password='user1senha')
        response = self.client.get(reverse('post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'blog/post_confirm_delete.html')

    def test_redirects_to_index_on_seccess(self):
        login = self.client.login(username='user1', password='user1senha')
        response = self.client.post(reverse('post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/blog/')


class CommentDeleteViewTest(TestCase):

    def setUp(self):
        # create users
        test_user = User.objects.create_user(username='user1', password='user1senha')
        test_user2 = User.objects.create_user(username='user2', password='user2senha')
        test_user2.save()
        test_user.save()

        # creats post

        self.post = Post.objects.create(
            title=f'post {1}',
            author=test_user
        )

        Comments.objects.create(blog_post=self.post, author=test_user, description='test comment!')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('comment-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/blog/post/comment/1/delete/')

    def test_redirect_if_logged_in_but_not_author_of_post(self):
        login = self.client.login(username='user2', password='user2senha')
        response = self.client.get(reverse('comment-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_and_author_of_post(self):
        login = self.client.login(username='user1', password='user1senha')
        response = self.client.get(reverse('comment-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_templte(self):
        login = self.client.login(username='user1', password='user1senha')
        response = self.client.get(reverse('comment-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/comments_confirm_delete.html')

    def test_redirects_to_detail_view_on_success(self):
        login = self.client.login(username='user1', password='user1senha')
        response = self.client.post(reverse('comment-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/blog/post/1/')

