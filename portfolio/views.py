from django.views.generic import TemplateView

# Create your views here.
class LoginPageView(TemplateView):
    template_name = 'login.html'

class MarketcapPageView(TemplateView):
    template_name = 'mc.html'