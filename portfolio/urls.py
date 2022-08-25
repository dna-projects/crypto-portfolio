from django.urls import path
from .views import LoginPageView, MarketcapBubblePageView, MarketcapPageView, PortfolioEditView 
from .views import MarketcapStatsPageView, PortfolioPageView, PortfolioStatsPageView, RegistrationPageView

urlpatterns = [
    # Entrypoints
    path("login", LoginPageView.as_view(), name="login"),
    path("registration", RegistrationPageView.as_view(), name="registration"),
    # Portfolio related...
    path("portfolio", PortfolioPageView.as_view(), name="portfolio"),
    path("asset/<int:pk>", PortfolioEditView.as_view(), name='asset_edit'),
    path("p-coin-stats", PortfolioStatsPageView.as_view(), name="p-coin-stats"),
    # Marketcap related...
    path("mc", MarketcapPageView.as_view(), name="mc"),
    path("mc-coin-stats", MarketcapStatsPageView.as_view(), name="mc-coin-stats"),
    path("mc-bubble", MarketcapBubblePageView.as_view(), name="mc-bubble"),
]