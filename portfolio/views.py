from pstats import Stats
from django.views.generic import TemplateView, CreateView, View, FormView
from portfolio.forms import UserRegistrationForm
from portfolio.forms import UserLoginForm
from portfolio.forms import NewTokenForm
from portfolio.models import AssetEntry
from django.shortcuts import render
from django.urls import reverse_lazy
import requests 
import json

# Entrypoints
class LoginPageView(FormView):
    template_name = 'login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('portfolio')

class RegistrationPageView(CreateView):
    template_name = 'registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

# Portfolio related...
class PortfolioPageView(CreateView):
    template_name = 'portfolio.html'
    form_class = NewTokenForm
    success_url = reverse_lazy('portfolio')

    def get(self, request):
        asset_entries = AssetEntry.objects.all()
        form = NewTokenForm()
        return render(request, self.template_name, {'asset_entries': asset_entries, 'form': form})

class PortfolioStatsPageView(TemplateView):
    template_name = 'p-coin-stats.html'

# Marketcap related...
# TODO think about using ABC (abstract base classes)
class MarketcapPageView(TemplateView):
    template_name = 'mc.html'
    
    def testAPI(self, request):
        # token_name = {'Ethereum': 'ethereum', 'Bitcoin': 'bitcoin'}
        # https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=USD
        # f"https://api.coingecko.com/api/v3/simple/price?ids={token_name}&vs_currencies=USD
        response = requests.get("")
        asset = json.loads(response.content)
        asset_name = asset['_name']
        # asset_name = 'coin gecko request for BTC coin name'
        asset_price = 'coin gecko request for BTC'
        return render(request, self.template_name, {'asset_name': asset_name, 'asset_price': asset_price})

class MarketcapStatsPageView(TemplateView):
    template_name = 'mc-coin-stats.html'

class MarketcapBubblePageView(TemplateView):
    template_name = 'mc-bubble.html'