from django import forms

from django_estates.blog.models import Comment
from django_estates.helpers.form_mixins import BootstrapFormsMixin, DisabledFieldsFormMixin


class CommentForm(forms.ModelForm, BootstrapFormsMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': 'Add comment'}
        widgets = {
            'text': forms.TextInput(
                attrs={'placeholder': 'Your comment...', }
            ),
        }


class DeleteCommentForm(forms.ModelForm, BootstrapFormsMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Comment
        fields = ()
