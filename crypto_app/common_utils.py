import random
import string
from crypto_auth.models import CustomUser


class CommonFunctionsMixin:
    def calculate_price_change(self, current_price, high_24h, low_24h):
        price_change_24h = None
        price_change_percentage_24h = None
        
        if current_price is not None and high_24h is not None and low_24h is not None:
            price_change_24h = high_24h - low_24h
            if low_24h > 0:
                price_change_percentage_24h = ((current_price - low_24h) / low_24h) * 100
        
        return price_change_24h, price_change_percentage_24h


class ReferralCodeGenerator:
    def __init__(self, code_length=8):
        self.code_length = code_length

    def generate_referral_code(self):
        while True:
            # Generate a random referral code
            characters = string.ascii_letters + string.digits
            referral_code = ''.join(random.choice(characters) for _ in range(self.code_length))

            # Check if the code is unique in the database
            if not CustomUser.objects.filter(referral_code=referral_code).exists():
                return referral_code