from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from django_estates.accounts.views import UserLoginView, UserRegisterView, profile_complete_view, ProfileDetailsView, \
    UserChangePasswordView, user_logout_view, ProfileEditView, favourite_add_view, favourites_list, ProfileDeleteView

urlpatterns = (
    # User main
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', user_logout_view, name='logout user'),
    path('register/', UserRegisterView.as_view(), name='register user'),
    path('change-password/', UserChangePasswordView.as_view(), name='change password'),
    path('password_change_done/', RedirectView.as_view(url=reverse_lazy('homepage')), name='password_change_done'),

    # Profile main
    path('profile-details/<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('profile-edit/<int:pk>/', ProfileEditView.as_view(), name='profile edit'),
    path('profile-delete/<int:pk>/', ProfileDeleteView.as_view(), name='profile delete'),

    # Side
    path('profile-complete/', profile_complete_view, name='profile complete'),
    path('favourites/<int:pk>/', favourite_add_view, name='favourite add'),
    path('profile/favourites/', favourites_list, name='favourite list'),

)
# Profile complete signal
import django_estates.accounts.signals
