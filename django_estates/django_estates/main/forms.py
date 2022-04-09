from django import forms
from django.forms import ClearableFileInput

from django_estates.helpers.form_mixins import BootstrapFormsMixin, DisabledFieldsFormMixin
from django_estates.main.models import Estate, EstateImages


class AddEstateForm(forms.ModelForm, BootstrapFormsMixin):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        # commit false does not persist in database
        # just returns the object to be created
        estate = super().save(commit=False)  # taking the estate instance

        estate.user = self.user
        if commit:
            estate.save()

        return estate

    class Meta:
        model = Estate
        exclude = ('user', 'publication_date', 'favourites')
        labels = {
            'title': 'Title',
            'type': 'Type',
            'location': 'Location',
            'floor': 'Floor',
            'heating_type': 'Heating type',
            'area': 'Area',
            'price': 'Price',
            'type_of_transaction': 'Type of transaction',
            'description': 'Description',
            'main_image': 'Main image',

        }


class AddEstateImagesForm(forms.ModelForm, BootstrapFormsMixin):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estate'].queryset = Estate.objects.filter(user=user)
        self._init_bootstrap_form_controls()

    class Meta:
        model = EstateImages
        fields = '__all__'
        widgets = {
            'image': ClearableFileInput(attrs={'multiple': True}),
        }
        labels = {
            'estate': 'Choose an estate',
            'image': 'Images',
        }


class EditEstateForm(forms.ModelForm, BootstrapFormsMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Estate
        exclude = ('user', 'publication_date', 'favourites')
        labels = {
            'title': 'Title',
            'type': 'Type',
            'location': 'Location',
            'floor': 'Floor',
            'heating': 'heating',
            'area': 'Area',
            'price': 'Price',
            'type_of_transaction': 'Type of transaction',
            'description': 'Description',
            'main_image': 'Main image',

        }


class DeleteEstateForm(forms.ModelForm, BootstrapFormsMixin, DisabledFieldsFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self._init_disabled_fields()

    def save(self, commit=True):
        photos = list(self.instance.estate_images_set.all())
        EstateImages.objects.filter(estate_id__in=photos).delete()
        self.instance.delete()
        # return self.instance

    class Meta:
        model = Estate
        fields = ()
