from django.contrib.auth import views as auth_views, logout
from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic as views

from django_estates.accounts.forms import UserLoginForm, UserRegisterForm, ProfileCompleteForm, PasswordEditForm, \
    ProfileEditForm, ProfileDeleteForm
from django_estates.accounts.models import Profile
from django_estates.main.models import Estate


# User main
class UserRegisterView(views.CreateView):
    form_class = UserRegisterForm
    template_name = 'accounts/user_register.html'
    success_url = reverse_lazy('login user')


class UserLoginView(auth_views.LoginView):
    form_class = UserLoginForm
    template_name = 'accounts/user_login.html'
    success_url = reverse_lazy('homepage')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


def user_logout_view(request):
    logout(request)
    return redirect('homepage')


class UserChangePasswordView(auth_views.PasswordChangeView):
    form_class = PasswordEditForm
    template_name = 'accounts/change_password.html'


# Profile main
class ProfileDetailsView(views.DetailView):
    model = Profile
    template_name = 'accounts/profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user == self.request.user
        estates = list(Estate.objects.filter(user_id=self.object.user_id))
        context.update({
            'estates': estates,
        })
        return context


class ProfileEditView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = Profile
    template_name = 'accounts/profile_edit.html'
    form_class = ProfileEditForm
    context_object_name = 'profile'

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.pk})


class ProfileDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = Profile
    form_class = ProfileDeleteForm
    template_name = 'accounts/profile_delete.html'
    success_url = reverse_lazy('homepage')


# Side
@login_required
def profile_complete_view(request):
    profile = Profile.objects.get(pk=request.user.id)
    if request.method == 'POST':
        form = ProfileCompleteForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = ProfileCompleteForm(instance=profile)

    context = {
        'form': form,
    }

    return render(request, 'accounts/profile_complete.html', context)


@login_required
def favourite_add_view(request, pk):
    estate = Estate.objects.get(id=pk)
    if estate.favourites.filter(id=request.user.id).exists():
        estate.favourites.remove(request.user)
    else:
        estate.favourites.add(request.user)
    return redirect('estate details', pk)


@login_required
def favourites_list(request):
    fav_estates = Estate.objects.filter(favourites=request.user)
    return render(request,
                  'accounts/favourites_list.html',
                  {'fav_estates': fav_estates})
