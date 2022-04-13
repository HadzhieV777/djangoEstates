from django.test import TestCase
from django.urls import reverse

from django_estates.newsletter.models import Subscribers


class SubscribeViewTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password': '1123QwER',
    }

    def test_correct_template__expect_success(self):
        response = self.client.get(reverse('subscribe'))
        self.assertTemplateUsed('newsletter/subscribe.html')
        self.assertTrue(response.status_code == 200)

    def test_add_subscriber__expect_success(self):
        subscriber = Subscribers.objects.create(email='testemail@gmail.com')
        self.client.post(reverse('subscribe'), {'email': 'testemail@gmail.com'})
        self.assertIsNotNone(subscriber.pk)

    def test_when_user_adds_email__expect_success(self):
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.post(
            reverse('subscribe'),
            data={
                'email': 'testemail@gmail.com',

            }
        )
        subscribers = Subscribers.objects.filter(email='testemail@gmail.com').exists()
        self.assertTrue(subscribers)
