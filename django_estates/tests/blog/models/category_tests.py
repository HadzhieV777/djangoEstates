from django.test import TestCase

from blog.models.helpers import create_category
from django_estates.blog.models import Category


class CategoryTests(TestCase):

    def test_category_creation__expect_success(self):
        category = create_category()
        self.assertTrue(isinstance(category, Category))
        self.assertIsNotNone(category.id)
