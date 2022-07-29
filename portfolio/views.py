from pstats import Stats
from django.views.generic import TemplateView, CreateView
from portfolio.forms import UserRegistrationForm
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
class PortfolioPageView(TemplateView):
    template_name = 'portfolio.html'
    asset_entries = AssetEntry.objects.all()

    def get(self, request):
        return render(request, self.template_name, {'asset_entries': self.asset_entries})
    
    # This will be used for the post request from the '+ Add Token' form 
    def post(self, request):
        # Need to create form and setup a local variable for it? or just use class
        # variable?
        # name = form.cleaned_data['name']
        # quantity = form.cleaned_data['quantity']
        name = ''
        quantity = ''
        price_at_purchase = ''
        # Maybe we need a 'current time' button
        datetime = ''

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