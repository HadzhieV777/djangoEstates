from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms
from django.contrib.auth.forms import SetPasswordForm

from django_estates.accounts.models import Profile
from django_estates.helpers.form_mixins import BootstrapFormsMixin, DisabledFieldsFormMixin
from django_estates.main.models import Estate


class UserRegisterForm(auth_forms.UserCreationForm, BootstrapFormsMixin):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(
            email=self.cleaned_data['email'],
            user=user,
        )

        if commit:
            profile.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'email')
        widgets = {
            'email': forms.TextInput(
                attrs={
                    'labels': 'Email',
                    'placeholder': 'Enter Email',
                }
            ),
        }


class UserLoginForm(auth_forms.AuthenticationForm, BootstrapFormsMixin):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'label': 'Username',
                }
            ),
            'password': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Password',
                }
            )
        }


class ProfileEditForm(forms.ModelForm, BootstrapFormsMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Profile
        exclude = ('is_complete', 'user', 'broker')


class ProfileDeleteForm(forms.ModelForm, DisabledFieldsFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_disabled_fields()

    def save(self, commit=True):
        Estate.objects.filter(user_id=self.instance.id).delete()

    class Meta:
        model = Profile
        fields = ()


class ProfileCompleteForm(forms.ModelForm, BootstrapFormsMixin):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Profile
        exclude = ('user', 'is_complete', 'email', 'broker')


class PasswordEditForm(auth_forms.PasswordChangeForm, BootstrapFormsMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['old_password', 'new_password1', 'new_password2']:
            self.fields[fieldname].help_text = None
        self._init_bootstrap_form_controls()

    error_messages = {
        **SetPasswordForm.error_messages,
        "password_incorrect": (
            "Your old password was entered incorrectly. Please enter it again."
        ),
    }
    old_password = forms.CharField(
        label=("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )

    field_order = ["old_password", "new_password1", "new_password2"]
