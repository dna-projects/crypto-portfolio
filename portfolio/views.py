from pstats import Stats
from django.views.generic import TemplateView, CreateView, View, FormView
from portfolio.forms import UserRegistrationForm
from portfolio.forms import UserLoginForm
from portfolio.forms import NewTokenForm
from portfolio.models import AssetEntry
from django.shortcuts import render
from django.urls import reverse_lazy
from dataclasses import dataclass
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
    
    @dataclass
    class TokenAPI:
        name: str
        symbol: str
        rank: int
        price: float
        one_hour_performance: float
        one_day_performance: float
        seven_day_performance: float
        one_day_volume: int
        marketcap: int
        
        def __init__(self, name):
            self.name = name
            response = requests.get(self.build_request())
            asset = json.loads(response.content)
            self.symbol = asset['symbol']
            self.rank = asset['market_cap_rank']
            self.price = asset['market_data']['current_price']['usd']

            # TODO need to find one hour performance
            # self.one_hour_performance = asset['market_data']['']
            self.one_day_performance = asset['market_data']['price_change_percentage_24h']
            self.seven_day_performance = asset['market_data']['price_change_percentage_7d']
            self.one_day_volume = asset['market_data']['total_volume']['usd']
            # TODO need to find 24h volume
            self.marketcap = asset['market_data']['market_cap']['usd']

        def build_request(self):
            return f"https://api.coingecko.com/api/v3/coins/{self.name}"

    def get(self, request):
        # token_name = {'Ethereum': 'ethereum', 'Bitcoin': 'bitcoin'}
        # https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=USD
        # f"https://api.coingecko.com/api/v3/simple/price?ids={token_name}&vs_currencies=USD
        
        # coin_gecko_list = ["ether", 'btc', 'solana']

        # token_list = []
        # for token_names in coin_gecko_list:
        #     token_list.append(self.TokenAPI(name=token_names))

        token_list = [
            self.TokenAPI(name="ethereum"),
            self.TokenAPI(name="bitcoin"),
            self.TokenAPI(name="solana")
        ]
        # # asset_name = 'coin gecko request for BTC coin name'
        # asset_price = 'coin gecko request for BTC'
        return render(request, self.template_name, {'token_list': token_list})

class MarketcapStatsPageView(TemplateView):
    template_name = 'mc-coin-stats.html'

class MarketcapBubblePageView(TemplateView):
    template_name = 'mc-bubble.html'