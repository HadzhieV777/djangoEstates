from django import forms

from django_estates.helpers.form_mixins import BootstrapFormsMixin
from django_estates.newsletter.models import Subscribers, MailMessage


class SubscribersForm(forms.ModelForm, BootstrapFormsMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['email']:
            self.fields[fieldname].help_text = None
        self._init_bootstrap_form_controls()

    class Meta:
        model = Subscribers
        fields = ('email',)
        labels = {
            'email': 'Email',
        }


class MailMessageForm(forms.ModelForm, BootstrapFormsMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = MailMessage
        fields = '__all__'
