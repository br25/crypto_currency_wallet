from django.contrib import admin
from .models import CryptoCurrency, Portfolio, Referral

# Register your models here
@admin.register(CryptoCurrency)
class CryptoCurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'current_price', 'high_24h', 'low_24h', 'price_change_24h', 'price_change_percentage_24h', 'last_updated')
    list_filter = ('name', 'symbol', 'last_updated')
    search_fields = ('name', 'symbol')

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'cryptocurrency', 'quantity', 'date_added')
    list_filter = ('user', 'cryptocurrency', 'date_added')
    search_fields = ('user__username', 'cryptocurrency__name', 'cryptocurrency__symbol')

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('referrer', 'referred_user', 'bonus_amount')
    list_filter = ('referrer', 'referred_user')
    search_fields = ('referrer__username', 'referred_user__username')

