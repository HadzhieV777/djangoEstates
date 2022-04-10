from django.urls import path

from django_estates.newsletter.views import subscribe_view, mail_letter_view

urlpatterns = (
    path('', subscribe_view, name='subscribe'),
    path('mail_letter/', mail_letter_view, name='mail letter')
)
