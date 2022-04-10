from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from django_estates.main.views.about import AboutPageView
from django_estates.main.views.estates import AddEstateView, AddEstatePhotosView, EstateDetailsView, EditEstateView, \
    DeleteEstateView

from django_estates.main.views.generic import HomepageView, EstatesGridView, AgentsGridView

urlpatterns = [
                  # Generic
                  path('', HomepageView.as_view(), name='homepage'),
                  path('estates/', EstatesGridView.as_view(), name='estates page'),
                  path('agents/', AgentsGridView.as_view(), name='agents page'),
                  path('about/', AboutPageView.as_view(), name='about page'),

                  # Estates Related
                  path('add-estate/', AddEstateView.as_view(), name='add estate'),
                  path('add-images/', AddEstatePhotosView.as_view(), name='upload images'),
                  path('edit-estate/<int:pk>/', EditEstateView.as_view(), name='edit estate'),
                  path('delete-estate/<int:pk>/', DeleteEstateView.as_view(), name='delete estate'),
                  path('estate-details/<int:pk>/', EstateDetailsView.as_view(), name='estate details'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
