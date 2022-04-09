from django.contrib.auth import get_user_model
from django.test import TestCase
from django_estates.blog.forms import DeleteCommentForm

UserModel = get_user_model()


class DeleteCommentFormTests(TestCase):

    def test_empty_form(self):
        form = DeleteCommentForm()

        self.assertNotIn('text', form.fields)
        self.assertNotIn('published', form.fields)
        self.assertNotIn('post', form.fields)
        self.assertNotIn('user', form.fields)
