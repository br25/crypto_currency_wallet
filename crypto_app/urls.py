from django.urls import path
from .views import crypto_views, portfolio_views

urlpatterns = [
    path('', crypto_views.CryptoCurrencyView.as_view(), name='crypto'),
    path('search/', crypto_views.CryptocurrencySearchView.as_view(), name='cryptocurrency-search'),
    # Wallet Api
    path('portfolio/', portfolio_views.PortfolioView.as_view(), name='add-to-portfolio'),
    #Referral Api
    # path('referral/', portfolio_views.ReferralView.as_view(), name='referral-list'),

]