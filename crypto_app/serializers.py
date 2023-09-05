from rest_framework import serializers
from .models import CryptoCurrency, Portfolio, Referral

class CryptoCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoCurrency
        fields = (
            'id',
            'image',
            'name',
            'symbol',
            'current_price',
            'high_24h',
            'low_24h',
            'price_change_24h',
            'price_change_percentage_24h',
        )

class PortfolioSerializer(serializers.ModelSerializer):
    user_username = serializers.SerializerMethodField()
    cryptocurrency_data = CryptoCurrencySerializer(source='cryptocurrency', read_only=True)

    class Meta:
        model = Portfolio
        fields = (
            'id',
            'user',
            'user_username',
            'cryptocurrency',
            'cryptocurrency_data',
            'quantity',
        )

    def get_user_username(self, obj):
        return obj.user.username

class ReferralSerializer(serializers.ModelSerializer):
    referrer_username = serializers.ReadOnlyField(source='referrer.username')
    referred_user_username = serializers.ReadOnlyField(source='referred_user.username')

    class Meta:
        model = Referral
        fields = ('id', 'bonus_amount', 'referrer', 'referred_user', 'referrer_username', 'referred_user_username')
