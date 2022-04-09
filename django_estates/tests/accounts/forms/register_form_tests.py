from django.test import TestCase

from django_estates.accounts.forms import UserRegisterForm


class RegisterFormTests(TestCase):

    def test_empty_form(self):
        form = UserRegisterForm()
        self.assertIn('username', form.fields)
        self.assertIn('password1', form.fields)
        self.assertIn('password2', form.fields)
        self.assertIn('email', form.fields)
        self.assertIn('class="form-control"', form.as_p())
