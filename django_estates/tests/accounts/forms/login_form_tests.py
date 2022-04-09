from django.test import TestCase

from django_estates.accounts.forms import UserLoginForm


class LoginFormTests(TestCase):

    def test_empty_form(self):
        form = UserLoginForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        self.assertIn('class="form-control"', form.as_p())
