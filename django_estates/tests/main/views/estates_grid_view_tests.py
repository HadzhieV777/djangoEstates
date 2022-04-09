from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

from django_estates.accounts.models import Profile
from django_estates.main.models import Estate

UserModel = get_user_model()


class EstatesGridViewTests(TestCase):
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
    VALID_POST_DATA = {
        "title": 'Test Title',
        'slug': slugify('Test Title'),
        'image': 'https://images.pexels.com/photos/1767434/pexels-photo-1767434.jpeg',
        'content': 'This is a test Post content. Nothing to see there!',
        'status': 1,
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

    def test_correct_template__expect_success(self):
        response = self.client.get(reverse('estates page'))
        self.assertTemplateUsed('main/estates_grid.html')
        self.assertTrue(response.status_code == 200)

    def test_create_estate_for_sale__expect_to_be_in_estates_for_sale(self):
        user, _ = self.__create_valid_user_and_profile()
        self.ESTATE_DATA['type_of_transaction'] = Estate.FOR_SALE
        estate = Estate.objects.create(
            **self.ESTATE_DATA,
            user=user,
        )
        response = self.client.get(reverse('estates page'))
        self.assertIn(estate, response.context['estates_for_sale'])

    def test_create_estate_for_rent__expect_to_be_in_estates_for_rent(self):
        user, _ = self.__create_valid_user_and_profile()
        self.ESTATE_DATA['type_of_transaction'] = Estate.FOR_RENT
        estate = Estate.objects.create(
            **self.ESTATE_DATA,
            user=user,
        )
        response = self.client.get(reverse('estates page'))
        self.assertIn(estate, response.context['estates_for_rent'])