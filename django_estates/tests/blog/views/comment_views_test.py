from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

from django_estates.accounts.models import Profile
from django_estates.blog.models import Post, Category, Comment

UserModel = get_user_model()


class AddAndDeleteCommentViewsTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testauthor',
        'password': '1123QwER',
    }
    SECOND_USER_CREDENTIALS = {
        'username': 'another_user',
        'password': '1123QwER',
    }

    VALID_POST_DATA = {
        "title": 'Test Title',
        'slug': slugify('Test Title'),
        'image': 'https://images.pexels.com/photos/1767434/pexels-photo-1767434.jpeg',
        'content': 'This is a test Post content. Nothing to see there!',
        'status': 1,
    }
    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'User',
        'image': 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&dpr=1&w'
                 '=500',
        'description': 'I am a test user',
        'email': 'test@gmail.com',
        'phone_number': '0878113344',
    }
    VALID_COMMENT_DATA = {
        'text': 'This is a test comment',
    }

    def setUp(self):
        # create permissions group
        group_name = "Users"
        self.group = Group(name=group_name)
        self.group.save()
        self.c = UserModel()

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )
        return (user, profile)

    def test_post_comment__if_valid__expect_to_be_created(self):
        user, _ = self.__create_valid_user_and_profile()
        category = Category.objects.create(title='A Test Category')
        post = Post.objects.create(
            **self.VALID_POST_DATA,
            category=category,
            author=user,
        )
        comment = Comment.objects.create(
            **self.VALID_COMMENT_DATA,
            post=post,
            user=user,
        )
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.post(
            reverse('comment post', kwargs={'slug': post.slug}),
            {'text': self.VALID_COMMENT_DATA['text']}
        )
        comment.refresh_from_db()
        self.assertEqual(comment.text, self.VALID_COMMENT_DATA['text'])

    def test_delete_comment__if_valid__expect_to_be_deleted(self):
        user, _ = self.__create_valid_user_and_profile()
        category = Category.objects.create(title='A Test Category')
        post = Post.objects.create(
            **self.VALID_POST_DATA,
            category=category,
            author=user,
        )
        comment = Comment.objects.create(
            **self.VALID_COMMENT_DATA,
            post=post,
            user=user,
        )
        self.client.login(**self.VALID_USER_CREDENTIALS)
        self.client.post(
            reverse('comment post', kwargs={'slug': post.slug}),
            {'text': self.VALID_COMMENT_DATA['text']}
        )
        comment.refresh_from_db()
        self.assertEqual(comment.text, self.VALID_COMMENT_DATA['text'])
        self.client.post(reverse('delete comment', kwargs={
            'pk': comment.id,
        }))
        response = self.client.get(reverse('post detail', kwargs={
            'slug': post.slug,
        }))
        self.assertTrue(response.context['comments_count'] == 0)

    def test_delete_comment__if_another_user__expect_to_not_delete_comment(self):
        user, profile = self.__create_valid_user_and_profile()
        category = Category.objects.create(title='A Test Category')
        post = Post.objects.create(
            **self.VALID_POST_DATA,
            category=category,
            author=user,
        )
        comment = Comment.objects.create(
            **self.VALID_COMMENT_DATA,
            post=post,
            user=user,
        )
        self.client.login(**self.VALID_USER_CREDENTIALS)
        self.client.post(
            reverse('comment post', kwargs={'slug': post.slug}),
            {'text': self.VALID_COMMENT_DATA['text']}
        )
        comment.refresh_from_db()
        self.assertEqual(comment.text, self.VALID_COMMENT_DATA['text'])
        self.client.logout()
        self.client.login(**self.SECOND_USER_CREDENTIALS)
        self.client.post(reverse('delete comment', kwargs={
            'pk': comment.id,
        }))

        response = self.client.get(reverse('post detail', kwargs={
            'slug': post.slug,
        }))

        self.assertTrue(response.context['comments_count'] == 1)

