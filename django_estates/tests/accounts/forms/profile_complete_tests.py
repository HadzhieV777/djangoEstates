from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from django_estates.accounts.forms import ProfileCompleteForm
from django_estates.accounts.models import Profile

UserModel = get_user_model()


class ProfileCompleteFormTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password': '1123QwER',
    }
    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': '',
        'image': 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&dpr=1&w'
                 '=500',
        'description': '',
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
        form = ProfileCompleteForm()

        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('image', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('phone_number', form.fields)

        self.assertNotIn('email', form.fields)
        self.assertNotIn('is_complete', form.fields)
        self.assertNotIn('user', form.fields)
        self.assertNotIn('broker', form.fields)
        self.assertIn('class="form-control"', form.as_p())

    def test_profile__when_empty_fields__expect_is_complete_false(self):
        user, profile = self.__create_valid_user_and_profile()
        self.assertTrue(user.profile.is_complete == False)

    def test_profile__when_no_empty_fields__expect_is_complete_true(self):
        self.VALID_PROFILE_DATA['last_name'] = 'User'
        self.VALID_PROFILE_DATA['description'] = 'Iam a test user'
        user, profile = self.__create_valid_user_and_profile()
        self.assertTrue(user.profile.is_complete == True)
