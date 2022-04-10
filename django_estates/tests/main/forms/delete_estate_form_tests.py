from django.contrib.auth import get_user_model
from django.test import TestCase
from django_estates.main.forms import DeleteEstateForm


UserModel = get_user_model()


class DeleteEstateFormTests(TestCase):

    def test_delete_form__when_valid__expect_true(self):
        form = DeleteEstateForm()

        self.assertNotIn('title', form.fields)
        self.assertNotIn('type', form.fields)
        self.assertNotIn('location', form.fields)
        self.assertNotIn('floor', form.fields)
        self.assertNotIn('heating_type', form.fields)
        self.assertNotIn('area', form.fields)
        self.assertNotIn('price', form.fields)
        self.assertNotIn('type_of_transaction', form.fields)
        self.assertNotIn('description', form.fields)
        self.assertNotIn('main_image', form.fields)
        self.assertNotIn('user', form.fields)
        self.assertNotIn('publication_date', form.fields)
        self.assertNotIn('favourites', form.fields)

