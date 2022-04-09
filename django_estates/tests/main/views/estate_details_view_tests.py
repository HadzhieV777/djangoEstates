from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from django_estates.accounts.models import Profile
from django_estates.main.models import Estate

UserModel = get_user_model()


class EstateDetailsView(TestCase):
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
    ESTATE_DATA = {
        'title': 'A great test Estate',
        'type': Estate.FOR_SALE,
        'location': 'Test zhk Test',
        'floor': Estate.ELEVENTH,
        'heating_type': Estate.FORCED_AIR_SYSTEMS,
        'area': 50,
        'exposition': Estate.NORTH,
        'price': 100000,
        'type_of_transaction': Estate.FOR_SALE,
        'description': 'This is a test estate!',
        'amenities': 'Test, Test, Test, Test',
        'main_image': 'test-image.jpg',
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

    def test_create_estate__if_valid__expect_to_render_correct_template(self):
        user, profile = self.__create_valid_user_and_profile()
        estate = Estate.objects.create(
            **self.ESTATE_DATA,
            user=user
        )

        self.client.get(reverse('estate details', kwargs={'pk': estate.pk}))
        self.assertIsNotNone(estate.pk)
        self.assertTemplateUsed('main/estates/estate_details.html')

    def test_context_data_price_per_sqm__expect_valid(self):
            user, profile = self.__create_valid_user_and_profile()
            estate = Estate.objects.create(
                **self.ESTATE_DATA,
                user=user
            )

            response = self.client.get(reverse('estate details', kwargs={'pk': estate.pk}))
            # self.assertTrue(response.context['amenities'] == self.ESTATE_DATA['amenities'])
            self.assertTrue(response.context['price_per_sqm'] == self.ESTATE_DATA['price'] / self.ESTATE_DATA['area'])

    def test_context_data_amenities__expect_valid(self):
            user, profile = self.__create_valid_user_and_profile()
            estate = Estate.objects.create(
                **self.ESTATE_DATA,
                user=user
            )

            response = self.client.get(reverse('estate details', kwargs={'pk': estate.pk}))
            self.assertListEqual(
                response.context['amenities'], list(self.ESTATE_DATA['amenities'].split(', '))
            )

    def test_context_data_estate_images__expect_valid(self):
            user, profile = self.__create_valid_user_and_profile()
            estate = Estate.objects.create(
                **self.ESTATE_DATA,
                user=user
            )

            response = self.client.get(reverse('estate details', kwargs={'pk': estate.pk}))
            self.assertListEqual(
                response.context['estate_images'], []
            )

