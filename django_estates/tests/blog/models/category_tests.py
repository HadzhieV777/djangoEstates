from django.test import TestCase


from django_estates.blog.models import Category


class CategoryTests(TestCase):

    def test_category_creation__expect_success(self):
        category = Category.objects.create(title='A Test Category')
        self.assertTrue(isinstance(category, Category))
        self.assertIsNotNone(category.id)
