from django.test import TestCase
from django.urls import reverse

from django_estates.newsletter.models import Subscribers


class SubscribeViewTests(TestCase):

    def test_correct_template__expect_success(self):
        response = self.client.get(reverse('subscribe'))
        self.assertTemplateUsed('newsletter/subscribe.html')
        self.assertTrue(response.status_code == 200)

    def test_add_subscriber__expect_success(self):
        subscriber = Subscribers.objects.create(email='testemail@gmail.com')
        self.client.post(reverse('subscribe'), {'email': 'testemail@gmail.com'})
        self.assertIsNotNone(subscriber.pk)

