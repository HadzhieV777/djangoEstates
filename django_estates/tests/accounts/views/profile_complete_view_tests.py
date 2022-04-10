from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from django_estates.accounts.models import Profile

UserModel = get_user_model()


class ProfileCompleteViewTests(TestCase):
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

    def test_view__when_profile_has_empty_fields__expect_is_complete_false(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('profile details', kwargs={
            'pk': profile.pk
        }))

        self.assertFalse(response.context['is_complete'])

    def test_view__when_profile_has_no_empty_fields__expect_is_complete_true(self):
        self.VALID_PROFILE_DATA['last_name'] = 'User'
        self.VALID_PROFILE_DATA['description'] = 'Iam a test user'
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('profile details', kwargs={
            'pk': profile.pk
        }))

        self.assertTrue(response.context['is_complete'])
