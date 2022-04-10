from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.test import TestCase

from django_estates.accounts.models import Profile

UserModel = get_user_model()


class ProfileModelTest(TestCase):
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

    def test_profile_full_name__when_valid__expect_full_name(self):
        self.VALID_PROFILE_DATA['first_name'] = 'Test'
        self.VALID_PROFILE_DATA['last_name'] = 'User'

        _, profile = self.__create_valid_user_and_profile()
        self.assertEqual('Test User', profile.full_name)

    def test_profile_create__when_first_name_contains_only_letters__expect_success(self):
        _, profile = self.__create_valid_user_and_profile()
        self.assertIsNotNone(profile.pk)

    def test_profile_create__when_first_name_contains_digit__expect_to_fail(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        self.VALID_PROFILE_DATA['first_name'] = 'Test2'
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()  # This is called in ModelForms implicitly but here we need to call it
            profile.save()
            self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_dollar_sign__expect_to_fail(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        self.VALID_PROFILE_DATA['first_name'] = 'Te$t'
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

    def test_profile_create__when_first_name_contains_only_one_letter__expect_to_fail(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        self.VALID_PROFILE_DATA['first_name'] = 'A'
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        with self.assertRaises(ValidationError):
            profile.full_clean()
            profile.save()

    def test_profile_create__when_last_name_contains_only_letters__expect_success(self):
        _, profile = self.__create_valid_user_and_profile()
        self.assertIsNotNone(profile.pk)

    def test_profile_create__when_last_name_contains_digit__expect_to_fail(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        self.VALID_PROFILE_DATA['last_name'] = 'User2'
        Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        self.assertRaisesRegex(ValidationError, Profile.ONLY_LETTERS_ERROR_MESSAGE)

    def test_profile_create__when_last_name_contains_dollar_sign__expect_to_fail(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        self.VALID_PROFILE_DATA['last_name'] = 'U$er'
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        with self.assertRaises(ValidationError):
            profile.full_clean()
            profile.save()

    def test_profile_create__when_last_name_contains_only_one_letter__expect_to_fail(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        self.VALID_PROFILE_DATA['last_name'] = 'U'
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        with self.assertRaises(ValidationError):
            profile.full_clean()
            profile.save()

    def test_profile_phone_number__when_valid__expect_success(self):
        _, profile = self.__create_valid_user_and_profile()
        self.assertIsNotNone(profile.pk)

    def test_profile_phone_number__if_incorrect_format__expect_to_fail(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        self.VALID_PROFILE_DATA['phone_number'] = '5444212456'
        Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        self.assertRaisesRegex(ValidationError, Profile.INVALID_NUMBER_ERROR_MESSAGE)

    def test_profile_is_complete__if_user_profile_completed__expect_success(self):
        _, profile = self.__create_valid_user_and_profile()
        self.assertTrue(profile.is_complete)
