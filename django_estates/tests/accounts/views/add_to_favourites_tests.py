from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from django_estates.accounts.models import Profile
from django_estates.main.models import Estate

UserModel = get_user_model()


class AddToFavouritesViewTests(TestCase):
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

    def test_when_user_add_estate__expect_estate_to_be_added_to_fav_list(self):
        user, profile = self.__create_valid_user_and_profile()
        estate = Estate.objects.create(
            **self.VALID_ESTATE_DATA,
            user=user,
        )
        self.client.post('favourite add', kwargs={'pk': estate.pk})
        self.assertTrue(self.client.get('estate details', kwargs={'pk': estate.pk}))
        self.assertIsNotNone(estate.favourites)

    def test_when__user_has_estates_in_favourites__expect_to_remove_it(self):
        user, profile = self.__create_valid_user_and_profile()
        estate = Estate.objects.create(
            **self.VALID_ESTATE_DATA,
            user=user,
        )
        self.client.post('favourite add', kwargs={'pk': estate.pk})
        self.assertTrue(self.client.get('estate details', kwargs={'pk': estate.pk}))
        self.assertIsNotNone(estate.favourites)
        self.client.post('favourite add', kwargs={'pk': estate.pk})
        self.client.get('estate details', kwargs={'pk': estate.pk})
        self.assertNotIn(user.pk, estate.favourites.all())

