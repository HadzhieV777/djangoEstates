from django.contrib import admin

# Register your models here.
from django_estates.newsletter.models import Subscribers, MailMessage

admin.site.register(MailMessage)
admin.site.register(Subscribers)
