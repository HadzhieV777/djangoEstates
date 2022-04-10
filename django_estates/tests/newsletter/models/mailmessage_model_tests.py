from django.test import TestCase

from django_estates.newsletter.models import MailMessage


class MailmessageModelTests(TestCase):
    VALID_MAILMESSAGE_DATA = {
        'title': 'Test',
        'message': 'Test message',
    }

    def test_mailmessage_creation__expect_success(self):
        mailmessage = MailMessage(
            **self.VALID_MAILMESSAGE_DATA,
        )
        self.assertIsNotNone(mailmessage)
        self.assertIsInstance(mailmessage, MailMessage)