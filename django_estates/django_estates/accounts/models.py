from django.contrib.auth import models as auth_models
from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models


from django_estates.accounts.managers import DjangoEstatesUserManager


class DjangoEstatesUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_MAX_LENGTH = 30

    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'username'

    objects = DjangoEstatesUserManager()


class Profile(models.Model):
    FIRST_NAME_MIN_LEN = 2
    FIRST_NAME_MAX_LEN = 30
    ONLY_LETTERS_ERROR_MESSAGE = "Ensure this value contains only letters."

    LAST_NAME_MIN_LEN = 2
    LAST_NAME_MAX_LEN = 30

    PHONE_NUMBER_MAX_LEN = 15
    INVALID_NUMBER_ERROR_MESSAGE = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LEN,
        null=True,
        blank=True,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LEN),
            RegexValidator(r'^[a-zA-Z]*$', ONLY_LETTERS_ERROR_MESSAGE),
        ),
    )
    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LEN,
        null=True,
        blank=True,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LEN),
            RegexValidator(r'^[a-zA-Z]*$', ONLY_LETTERS_ERROR_MESSAGE),
        ),
    )
    image = models.URLField(
        null=True,
        blank=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=PHONE_NUMBER_MAX_LEN,
        null=True,
        blank=True,
        validators=(
            RegexValidator(r'^\+?1?\d{9,15}$', INVALID_NUMBER_ERROR_MESSAGE),
        ),
    )
    broker = models.BooleanField(
        default=False,
    )
    is_complete = models.BooleanField(
        default=False,
    )
    user = models.OneToOneField(
        DjangoEstatesUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ('first_name', 'last_name',)