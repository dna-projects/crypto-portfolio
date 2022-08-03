from pstats import Stats
from django.views.generic import TemplateView, CreateView
from django.views.generic.edit import UpdateView
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
class PortfolioPageView(TemplateView):
    template_name = 'portfolio.html'
    form_class = NewTokenForm
    asset_entries = AssetEntry.objects.all()
    success_url = reverse_lazy('portfolio')

    def get(self, request):
        return render(request, self.template_name, {'asset_entries': self.asset_entries})

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