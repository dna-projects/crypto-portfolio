from django.views.generic import (
    TemplateView, 
    CreateView, 
    View, 
    FormView,
    UpdateView)
from django.views.generic.edit import DeletionMixin
from portfolio.forms import EditTokenForm, UserRegistrationForm, UserLoginForm, NewTokenForm
from portfolio.models import AssetEntry
from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse_lazy
import requests 
import json

# Landing
class LandingPageView(TemplateView):
    template_name = 'landing.html'

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
        # TODO - Need to make this update based on the current price from Coingecko
        # NOT the cost basis 
        balance = AssetEntry.objects.aggregate(total=Sum('cost_basis'))

        # Get token list from Coingecko
        # TODO - Run the api call only when opening the add token modal
        num_tokens = 15
        currency = 'usd'
        url_tokens = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency}&order=market_cap_desc&per_page={num_tokens}&page=1&sparkline=false"
        response = requests.get(url_tokens)
        asset = json.loads(response.content)

        tokens = {}
        for index, _ in enumerate(asset):
            tokens[asset[index]['name']] = asset[index]['id']

        form = NewTokenForm()
        form.updateChoices(tokens)
        return render(request, self.template_name, {
            'asset_entries': asset_entries, 
            'form': form,
            'tokens': tokens,
            'balance': balance
            })

class PortfolioEditView(DeletionMixin, UpdateView):
    model = AssetEntry
    template_name = 'portfolio-edit.html'
    form_class = EditTokenForm
    success_url = reverse_lazy('portfolio')

    # Create a get method that uses the current object's model name 
    # to display in the template
    # def get(self, request):
    #   current_asset = # get object somehow
    #   return render(request, self.template_name, {'current_asset': current_asset})

    def post(self, request, pk, *args, **kwargs):
        if "delete" in self.request.POST:
            return super().post(request, pk)
        elif "update" in self.request.POST:
            return UpdateView.post(self, request, *args, **kwargs)

class PortfolioStatsPageView(TemplateView):
    template_name = 'p-coin-stats.html'

# Marketcap related...
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
                self.one_day_performance = asset[index]['price_change_percentage_24h']
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

    def call_coin_gecko(self, page=1): # Other possible input?
        # Make request to coin gecko API for the token list up to top 15 tokens
        num_tokens = 15
        currency = 'usd'
        source_list = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency}&order=market_cap_desc&per_page={num_tokens}&page={page}&sparkline=false"
        response = requests.get(source_list)
        return json.loads(response.content)

    def get(self, request):
        asset = self.call_coin_gecko(2)
        token_list = []
        for index, _ in enumerate(asset):
            token_list.append(self.TokenAPI(index=index, request=asset, mockup=False))

        return render(request, self.template_name, {'token_list': token_list})

    # TODO - This is buggy right now because the return isn't working
    def update(self, request, num):
        print("Updating page...")
        return render(request, self.template_name)

class MarketcapStatsPageView(TemplateView):
    template_name = 'mc-coin-stats.html'

class MarketcapBubblePageView(TemplateView):
    template_name = 'mc-bubble.html'