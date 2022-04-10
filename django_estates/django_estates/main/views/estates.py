from django.contrib.auth import mixins as auth_mixins
from django.urls import reverse_lazy

from django_estates.accounts.models import Profile
from django_estates.main.forms import AddEstateForm, AddEstateImagesForm, EditEstateForm, DeleteEstateForm
from django.views import generic as views

from django_estates.main.models import Estate, EstateImages


class AddEstateView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.CreateView):
    permission_required = 'main.add_estate'
    template_name = 'main/estates/add_estate.html'
    form_class = AddEstateForm
    success_url = reverse_lazy('homepage')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.user_id})


class AddEstatePhotosView(auth_mixins.LoginRequiredMixin, views.CreateView):
    form_class = AddEstateImagesForm
    template_name = 'main/estates/add_estate_photos.html'
    success_url = reverse_lazy('estates page')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EstateDetailsView(views.DetailView):
    model = Estate
    template_name = 'main/estates/estate_details.html'
    context_object_name = 'estate'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user == self.request.user
        estate_images = list(EstateImages.objects.filter(estate_id=self.object.id))
        seller = Profile.objects.filter(user_id=self.object.user_id).first()
        amenities = self.object.amenities.split(", ")
        price_per_sqm = self.object.price / self.object.area

        context.update({
            'estate_images': estate_images,
            'seller': seller,
            'amenities': amenities,
            'price_per_sqm': price_per_sqm,
        })

        return context


class EditEstateView(views.UpdateView, auth_mixins.LoginRequiredMixin):
    model = Estate
    template_name = 'main/estates/edit_estate.html'
    form_class = EditEstateForm

    def get_success_url(self):
        return reverse_lazy('estate details', kwargs={'pk': self.object.id})


class DeleteEstateView(views.DeleteView, auth_mixins.LoginRequiredMixin):
    model = Estate
    template_name = 'main/estates/estate_delete.html'
    form_class = DeleteEstateForm

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.user_id})
