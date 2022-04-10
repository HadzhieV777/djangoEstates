from django.contrib.auth import get_user_model
from django.test import TestCase
from django_estates.blog.forms import CommentForm

UserModel = get_user_model()


class CommentFormTests(TestCase):

    def test_empty_form(self):
        form = CommentForm()

        self.assertIn('text', form.fields)

        self.assertNotIn('published', form.fields)
        self.assertNotIn('post', form.fields)
        self.assertNotIn('user', form.fields)
        self.assertIn('class="form-control"', form.as_p())
