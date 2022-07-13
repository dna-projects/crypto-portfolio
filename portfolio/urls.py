from django.urls import path
from .views import LoginPageView, MarketcapPageView

urlpatterns = [
    path("mc", MarketcapPageView.as_view(), name="mc"),
    path("login", LoginPageView.as_view(), name="login")
    
]