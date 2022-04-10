from django.test import TestCase

from django_estates.newsletter.forms import MailMessageForm


class MailMessageFormTests(TestCase):

    def test_empty_form(self):
        form = MailMessageForm()

        self.assertIn('title', form.fields)
        self.assertIn('message', form.fields)
        self.assertIn('class="form-control"', form.as_p())

