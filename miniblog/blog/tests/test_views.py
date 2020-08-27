from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.utils import timezone

from blog.models import Post, Comments
from blog.forms import CreateComments


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

    @classmethod
    def setUpTestData(cls):
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
        self.assertRedirects(response, reverse('post-detail', kwargs={'pk': '1'}))

