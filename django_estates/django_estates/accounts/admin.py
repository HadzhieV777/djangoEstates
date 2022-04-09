from django.contrib import admin

from django_estates.accounts.models import Profile, DjangoEstatesUser


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'first_name')


@admin.register(DjangoEstatesUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    filter_horizontal = ("groups", "user_permissions")
