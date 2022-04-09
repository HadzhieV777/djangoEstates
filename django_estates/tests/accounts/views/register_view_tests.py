from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()


class ProfileCreateViewTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password1': '1123QwER',
        'password2': '1123QwER',
        'email': 'test@test.com'
    }
    LOGIN_CREDENTIALS = {
        'username': 'testuser',
        'password': '1123QwER'}
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

    def test_register__when_all_valid__expect_success(self):
        self.client.post(
            reverse('register user'),
            data=self.VALID_USER_CREDENTIALS,
        )
        user = self.client.login(**self.LOGIN_CREDENTIALS)
        self.assertIsNotNone(user)
