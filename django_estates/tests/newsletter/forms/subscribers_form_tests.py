from django.test import TestCase

from django_estates.newsletter.forms import SubscribersForm


class SubscribersFormTests(TestCase):

    def test_empty_form(self):
        form = SubscribersForm()

        self.assertIn('email', form.fields)
        self.assertNotIn('date', form.fields)
        self.assertIn('class="form-control"', form.as_p())