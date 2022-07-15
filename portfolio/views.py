from pstats import Stats
from django.views.generic import TemplateView

# Entrypoints
class LoginPageView(TemplateView):
    template_name = 'login.html'

class RegistrationPageView(TemplateView):
    template_name = 'registration.html'

# Portfolio related...
class PortfolioPageView(TemplateView):
    template_name = 'portfolio.html'

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