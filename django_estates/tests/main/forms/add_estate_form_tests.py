from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django_estates.accounts.models import Profile
from django_estates.main.forms import AddEstateForm

UserModel = get_user_model()


class AddEstateFormTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password': '1123QwER',
    }
    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'User',
        'image': 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&dpr=1&w'
                 '=500',
        'description': 'I am a test user',
        'email': 'test@gmail.com',
        'phone_number': '0878113344',
    }

    def setUp(self):
        # create permissions group
        group_name = "Users"
        self.group = Group(name=group_name)
        self.group.save()
        self.c = UserModel()

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )
        return (user, profile)

    def test_empty_form(self):
        user, profile = self.__create_valid_user_and_profile()
        form = AddEstateForm(user=user)

        self.assertIn('title', form.fields)
        self.assertIn('type', form.fields)
        self.assertIn('location', form.fields)
        self.assertIn('floor', form.fields)
        self.assertIn('heating_type', form.fields)
        self.assertIn('area', form.fields)
        self.assertIn('price', form.fields)
        self.assertIn('type_of_transaction', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('main_image', form.fields)

        self.assertNotIn('user', form.fields)
        self.assertNotIn('publication_date', form.fields)
        self.assertNotIn('favourites', form.fields)
        self.assertIn('class="form-control"', form.as_p())
