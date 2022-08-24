from lib2to3.pgen2 import token
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

        # Get token list from Coingecko
        # TODO - Run the api call only when opening the add token modal
        num_tokens = 15
        currency = 'usd'
        url_tokens = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency}&order=market_cap_desc&per_page={num_tokens}&page=1&sparkline=false"
        response = requests.get(url_tokens)
        asset = json.loads(response.content)

        # TODO - Default value is able to submit the form...
        tokens = {'-- Select token --': ''}
        for index, _ in enumerate(asset):
            tokens[asset[index]['name']] = asset[index]['id']

        form = NewTokenForm()
        form.updateChoices(tokens)
        return render(request, self.template_name, {
            'asset_entries': asset_entries, 
            'form': form,
            'tokens': tokens
            })

class PortfolioStatsPageView(TemplateView):
    template_name = 'p-coin-stats.html'

# Marketcap related...
# TODO think about using ABC (abstract base classes)
class MarketcapPageView(TemplateView):
    template_name = 'mc.html'
    
    class TokenAPI:
        def __init__(self, index, request, mockup=False):
            if not mockup:
                asset = request
                self.name = asset[index]['name']
                self.symbol = asset[index]['symbol']
                self.rank = asset[index]['market_cap_rank']
                self.price = asset[index]['current_price']
                if self.price > 0.01:
                    self.price = f"${self.price:,.2f}"
                else:
                    self.price = f"${self.price:.7f}"
                # self.one_hour_performance = f"{asset[index]['price_change_percentage_1h_in_currency']:.1f}%"
                self.one_day_performance = f"{asset[index]['price_change_percentage_24h']:.1f}%"
                # self.seven_day_performance = f"{asset[index]['price_change_percentage_7d']:.1f}%"
                self.one_day_volume = f"{asset[index]['total_volume']:,}"
                self.marketcap = f"{asset[index]['market_cap']:,}"
            else:
                self.build_mockup()

        def build_mockup(self):
            self.name = 'Solana';
            self.symbol = 'SOL'
            self.rank = 9
            self.price = '43.31'
            # mockup_one_hour_performance = 0.19999999
            # self.one_hour_performance = f'{mockup_one_hour_performance:.1f}%'
            self.one_day_performance = '-1.31881'
            # self.seven_day_performance = '6.95958'
            mockup_one_day_vol = 4975982338375
            self.one_day_volume = f"{mockup_one_day_vol:,}"
            mockup_mc = 15069857156
            self.marketcap = f"{mockup_mc:,}"


    def get(self, request):        
        # Make request to coin gecko API for the token list up to top 15 tokens
        num_tokens = 15
        currency = 'usd'
        source_list = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency}&order=market_cap_desc&per_page={num_tokens}&page=1&sparkline=false"
        response = requests.get(source_list)
        asset = json.loads(response.content)
        
        token_list = []
        for index, _ in enumerate(asset):
            token_list.append(self.TokenAPI(index=index, request=asset, mockup=False))

        return render(request, self.template_name, {'token_list': token_list})

class MarketcapStatsPageView(TemplateView):
    template_name = 'mc-coin-stats.html'

class MarketcapBubblePageView(TemplateView):
    template_name = 'mc-bubble.html'