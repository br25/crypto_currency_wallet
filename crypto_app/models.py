from django.db import models
from crypto_auth.models import CustomUser as User

class CryptoCurrency(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    image = models.URLField()
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    current_price = models.DecimalField(max_digits=10, decimal_places=4)
    high_24h = models.DecimalField(max_digits=10, decimal_places=4)
    low_24h = models.DecimalField(max_digits=10, decimal_places=4)
    price_change_24h = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    price_change_percentage_24h = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cryptocurrency = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)  # Added date and time

    def __str__(self):
        return f"{self.user.username}'s Portfolio: {self.quantity} {self.cryptocurrency.name}"

class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals')
    referred_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred_by')
    bonus_amount = models.DecimalField(max_digits=20, decimal_places=10)
    
    def __str__(self):
        return f"{self.referrer.username} referred {self.referred_user.username}"
