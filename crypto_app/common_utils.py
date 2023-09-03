class CommonFunctionsMixin:
    def calculate_price_change(self, current_price, high_24h, low_24h):
        price_change_24h = None
        price_change_percentage_24h = None
        
        if current_price is not None and high_24h is not None and low_24h is not None:
            price_change_24h = high_24h - low_24h
            if low_24h > 0:
                price_change_percentage_24h = ((current_price - low_24h) / low_24h) * 100
        
        return price_change_24h, price_change_percentage_24h
