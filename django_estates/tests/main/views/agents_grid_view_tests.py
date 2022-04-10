from django.test import TestCase

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

from django_estates.accounts.models import Profile

UserModel = get_user_model()


class AgentsGridViewTests(TestCase):
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

    def test_correct_template__expect_success(self):
        response = self.client.get(reverse('agents page'))
        self.assertTemplateUsed('main/agents_grid.html')
        self.assertTrue(response.status_code == 200)

    def test_add_user__if_broker_true__expect_user_in_agents_grid(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        self.VALID_PROFILE_DATA['broker'] = True
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )
        self.assertIsNotNone(profile.pk)
        response = self.client.get(reverse('agents page'))
        self.assertIn(profile, response.context['agents'])
        self.assertTrue(response.context['agents'][0] == profile)
        self.assertTrue(response.context['agents'].exists())

    def test_add_user__if_broker_false__expect_user_not_in_agents_grid(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        self.VALID_PROFILE_DATA['broker'] = False
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )
        self.assertIsNotNone(profile.pk)
        response = self.client.get(reverse('agents page'))
        self.assertNotIn(profile, response.context['agents'])
        self.assertFalse(response.context['agents'].exists())
