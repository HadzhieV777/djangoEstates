from django.contrib.auth import mixins as auth_mixins
from django.views import generic as views


class AboutPageView(views.TemplateView):
    template_name = 'main/about_test.html'
