from django.contrib import admin

from django_estates.main.models import Estate, EstateImages


@admin.register(Estate)
class EstateAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'type_of_transaction')


@admin.register(EstateImages)
class EstateImageAdmin(admin.ModelAdmin):
    model = EstateImages
    list_display = ('estate',)
