from pstats import Stats
from django.views.generic import TemplateView, CreateView, View, FormView
from portfolio.forms import UserRegistrationForm
from portfolio.forms import NewTokenForm
from portfolio.models import AssetEntry
from django.shortcuts import render
from django.urls import reverse_lazy

# Entrypoints
class LoginPageView(TemplateView):
    template_name = 'login.html'

class RegistrationPageView(CreateView):
    template_name = 'registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

# Portfolio related...
class PortfolioPageView(CreateView):
    template_name = 'portfolio.html'
    form_class = NewTokenForm
    success_url = reverse_lazy('portfolio')

    # TODO - Last update: 8/4/22
    # Having issues with showing the form AND showing the asset entries at the same time
    # 
    # Our custom get request needs to:
    # 1. Grab the asset entries
    # 2. Grab the form fields (I'm thinking this is why it's missing from the html)
    #   a. Manually coding the get/post request for a form
    def get(self, request, *args, **kwargs):
        print('Get request successful')
        view = PortfolioPageTemplateView.as_view()
        return view(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     print('Post request successful')
    #     view = PortfolioPageCreateView.as_view()
    #     return view(request, *args, **kwargs)

class PortfolioPageTemplateView(TemplateView):
    template_name = 'portfolio.html'
    asset_entries = AssetEntry.objects.all()

    def get(self, request):
        return render(request, self.template_name, {'asset_entries': self.asset_entries})

# Form
class PortfolioPageCreateView(FormView):
    template_name = 'portfolio.html'
    form_class = NewTokenForm
    success_url = reverse_lazy('portfolio')

class PortfolioStatsPageView(TemplateView):
    template_name = 'p-coin-stats.html'

# Marketcap related...
# TODO think about using ABC (abstract base classes)
class MarketcapPageView(TemplateView):
    template_name = 'mc.html'

class MarketcapStatsPageView(TemplateView):
    template_name = 'mc-coin-stats.html'

class MarketcapBubblePageView(TemplateView):
    template_name = 'mc-bubble.html'