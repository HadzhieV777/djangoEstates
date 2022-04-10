from django.test import TestCase

from django_estates.newsletter.models import Subscribers


class SubscribersModelTests(TestCase):

    def test_subscribers_creation__expect_success(self):
        subscriber = Subscribers.objects.create(email='testemail@gmail.com')
        self.assertTrue(isinstance(subscriber, Subscribers))
        self.assertIsNotNone(subscriber.id)