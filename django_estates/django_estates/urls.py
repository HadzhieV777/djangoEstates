from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django_estates.main.urls')),
    path('accounts/', include('django_estates.accounts.urls')),
    path('blog/', include('django_estates.blog.urls')),
    path('newsletter/', include('django_estates.newsletter.urls')),
]
