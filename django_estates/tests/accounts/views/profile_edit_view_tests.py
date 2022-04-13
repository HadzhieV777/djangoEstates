from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from django_estates.accounts.models import Profile

UserModel = get_user_model()


class ProfileEditViewTests(TestCase):
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

    def test_when_all_valid__expect_correct_template(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        self.client.get(reverse('profile edit', kwargs={
            'pk': profile.pk,
        }))
        self.assertTemplateUsed('accounts/profile_edit.html')

    def test_if_user_edit_profile_first_name__expect_success(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.post(
            reverse('profile edit', kwargs={
                'pk': profile.pk,
            }),
            data={
                'first_name': 'Changed',
                'last_name': 'Names',
                'image': 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&dpr=1&w'
                         '=500',
                'description': 'Changed',
                'email': 'test@gmail.com',
                'phone_number': '0878113344',
            }
        )
        user_profile = Profile.objects.get(pk=profile.pk)
        self.assertEqual('Changed', user_profile.first_name)
