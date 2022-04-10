from django.test import TestCase
from django.urls import reverse

from django_estates.newsletter.models import MailMessage


class MailLetterViewTests(TestCase):
    VALID_MAILMESSAGE_DATA = {
        'title': 'Test',
        'message': 'Test message',
    }

    def test_correct_template__expect_success(self):
        response = self.client.get(reverse('mail letter'))
        self.assertTemplateUsed('newsletter/mail_letter.html')
        self.assertTrue(response.status_code == 200)

    def test_mail_letter_creation__expect_success(self):
        mailmessage = MailMessage(
            **self.VALID_MAILMESSAGE_DATA,
        )
        self.client.get(reverse('mail letter'), {'title': 'Test', 'message': 'Test message'})
        self.assertTrue(mailmessage.title == self.VALID_MAILMESSAGE_DATA['title'])
        self.assertTrue(mailmessage.message == self.VALID_MAILMESSAGE_DATA['message'])