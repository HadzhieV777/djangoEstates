from django.views import generic as views

from django_estates.accounts.models import Profile
from django_estates.blog.models import Post
from django_estates.main.models import Estate


class HomepageView(views.ListView):
    template_name = 'main/homepage.html'
    model = Estate

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estates = Estate.objects.all()
        blog = Post.objects.all()

        context.update({
            'estates': estates,
            'blog': blog,
        })

        return context


class EstatesGridView(views.ListView):
    model = Estate
    template_name = 'main/estates_grid.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for_rent = Estate.objects.all().filter(type_of_transaction=Estate.FOR_RENT)
        for_sale = Estate.objects.all().filter(type_of_transaction=Estate.FOR_SALE)
        context.update({
            'estates_for_rent': for_rent,
            'estates_for_sale': for_sale,

        })

        return context


class AgentsGridView(views.ListView):
    model = Profile
    template_name = 'main/agents_grid.html'
    context_object_name = 'agents'

    def get_queryset(self):
        queryset = Profile.objects.filter(broker=True)
        return queryset

