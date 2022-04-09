from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from django_estates.accounts.models import Profile
from django_estates.main.models import Estate

UserModel = get_user_model()


class ProfileDetailsViewTests(TestCase):
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
    SECOND_PROFILE_DATA = {
        'first_name': 'Another',
        'last_name': 'User',
        'image': 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&dpr=1&w'
                 '=500',
        'description': 'I am a test user',
        'email': 'another@gmail.com',
        'phone_number': '0878113344',
    }

    VALID_ESTATE_DATA = {
        'title': 'Test Estate Title',
        'type': Estate.TWO_BEDROOMS_APARTMENT,
        'location': 'Test zhk Test',
        'floor': Estate.THIRD,
        'heating_type': Estate.ELECTRIC_SYSTEM,
        'area': 100,
        'exposition': Estate.SOUTH,
        'price': 100000,
        'type_of_transaction': Estate.FOR_SALE,
        'description': 'This is a test Estate, its not for sale',
        'amenities': 'Test, Test, Test, Test',
        'main_image': 'test.jpg',
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
        self.client.get(reverse('profile details', kwargs={
            'pk': profile.pk,
        }))
        self.assertTemplateUsed('accounts/profile_edit.html')

    def test_when_user__is_owner__should_be_true(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('profile details', kwargs={
            'pk': profile.pk
        }))

        self.assertTrue(response.context['is_owner'])

    def test_when_user_is_not_owner__expect_is_owner_to_be_false(self):
        _, profile = self.__create_valid_user_and_profile()
        credentials = {
            'username': 'testuser2',
            'password': '12345qwe',
        }
        second_user = self.__create_user(**credentials)
        second_profile = Profile.objects.create(
            **self.SECOND_PROFILE_DATA,
            user=second_user,
        )

        self.client.login(**credentials)

        response = self.client.get(reverse('profile details', kwargs={
            'pk': profile.pk
        }))

        self.assertFalse(response.context['is_owner'])

    def test_when_no_estates__estates__should_be_empty(self):
        _, profile = self.__create_valid_user_and_profile()
        credentials = {
            'username': 'testuser2',
            'password': '12345qwe',
        }
        second_user = self.__create_user(**credentials)
        second_profile = Profile.objects.create(
            **self.SECOND_PROFILE_DATA,
            user=second_user,
        )
        self.client.login(**credentials)
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))
        self.assertListEqual(
            [],
            response.context['estates'],
        )

    def test_when_estates__estates__should_be_owner_estates(self):
        user, profile = self.__create_valid_user_and_profile()
        credentials = {
            'username': 'testuser2',
            'password': '12345qwe',
        }
        second_user = self.__create_user(**credentials)
        second_profile = Profile.objects.create(
            **self.SECOND_PROFILE_DATA,
            user=second_user,
        )

        estate = Estate.objects.create(
            **self.VALID_ESTATE_DATA,
            user=second_user
        )
        self.client.login(**credentials)
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

        self.assertIsNotNone(
            response.context['estates'],
        )

