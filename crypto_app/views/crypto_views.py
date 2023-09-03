from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
import logging
import requests
from ..models import CryptoCurrency
from ..serializers import CryptoCurrencySerializer
from ..common_utils import CommonFunctionsMixin


class CryptoCurrencyView(CommonFunctionsMixin, APIView):
    def get(self, request):
        url = 'https://api.coingecko.com/api/v3/coins/markets'

        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 10,
            'page': 1,
            'sparkline': False,
            'price_change_percentage': '24h',
            'locale': 'en',
        }

        try:
            response = requests.get(url, params=params)

            # Check if the response status code is 200 (OK)
            if response.status_code == 200:
                response_json = response.json()

                # Loop through the data
                for currency_detail in response_json:
                    # Calculate price change
                    price_change_24h, price_change_percentage_24h = self.calculate_price_change(
                        currency_detail.get('current_price'),
                        currency_detail.get('high_24h'),
                        currency_detail.get('low_24h')
                    )

                    # Try to get the cryptocurrency by symbol
                    cryptocurrency, created = CryptoCurrency.objects.get_or_create(
                        symbol=currency_detail['symbol'],
                        defaults={
                            'id': currency_detail['id'],
                            'image': currency_detail['image'],
                            'name': currency_detail['name'],
                            'current_price': currency_detail['current_price'],
                            'high_24h': currency_detail['high_24h'],
                            'low_24h': currency_detail['low_24h'],
                            'price_change_24h': price_change_24h,
                            'price_change_percentage_24h': price_change_percentage_24h,
                        }
                    )

                    # If the cryptocurrency already exists, update its fields
                    if not created:
                        cryptocurrency.id = currency_detail['id']
                        cryptocurrency.image = currency_detail['image']
                        cryptocurrency.name = currency_detail['name']
                        cryptocurrency.current_price = currency_detail['current_price']
                        cryptocurrency.high_24h = currency_detail['high_24h']
                        cryptocurrency.low_24h = currency_detail['low_24h']
                        cryptocurrency.price_change_24h = price_change_24h
                        cryptocurrency.price_change_percentage_24h = price_change_percentage_24h
                        cryptocurrency.save()

                # Continue with your existing code
                filtered_data = [{'id': currency_detail['id'], 'image': currency_detail['image'], 'name': currency_detail['name'], 'symbol': currency_detail['symbol'], 'current_price': currency_detail['current_price'], 'high_24h': currency_detail['high_24h'], 'low_24h': currency_detail['low_24h'], 'price_change_24h': price_change_24h, 'price_change_percentage_24h': price_change_percentage_24h} for currency_detail in response_json]
                # For Drf
                # return Response(filtered_data, status=status.HTTP_200_OK)
                
                # For Html
                context = {
                    'crypto_currencies': filtered_data, 
                }
                return render(request, 'crypto_currency.html', context)
            else:
                error_message = f'Failed to status'
                logging.error(error_message)
                return Response({'error':error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except requests.exceptions.RequestException as e:
            error_message = f'Failed fetch'
            logging.error(error_message)
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CryptocurrencySearchView(CommonFunctionsMixin, APIView):
    def get(self, request):
        query = self.request.query_params.get('query', None)
        if query is not None:
            query = query.lower()
        if not query:
            return Response({'error': 'Query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Customize the URL based on the query parameter
        url = f'https://api.coingecko.com/api/v3/coins/markets?ids={query}&vs_currency=usd'

        try:
            response = requests.get(url)

            if response.status_code == 200:
                response_json = response.json()
                

                for currency_detail in response_json:
                    # Calculate price change
                    price_change_24h, price_change_percentage_24h = self.calculate_price_change(
                        currency_detail.get('current_price'),
                        currency_detail.get('high_24h'),
                        currency_detail.get('low_24h')
                    )

                    # Try to get the cryptocurrency by symbol
                    cryptocurrency, created = CryptoCurrency.objects.get_or_create(
                        symbol=currency_detail['symbol'],
                        defaults={
                            'id': currency_detail['id'],
                            'image': currency_detail['image'],
                            'name': currency_detail['name'],
                            'current_price': currency_detail['current_price'],
                            'high_24h': currency_detail['high_24h'],
                            'low_24h': currency_detail['low_24h'],
                            'price_change_24h': price_change_24h,
                            'price_change_percentage_24h': price_change_percentage_24h,
                        }
                    )

                    # If the cryptocurrency already exists, update its fields
                    if not created:
                        cryptocurrency.id = currency_detail['id']
                        cryptocurrency.image = currency_detail['image']
                        cryptocurrency.name = currency_detail['name']
                        cryptocurrency.current_price = currency_detail['current_price']
                        cryptocurrency.high_24h = currency_detail['high_24h']
                        cryptocurrency.low_24h = currency_detail['low_24h']
                        cryptocurrency.price_change_24h = price_change_24h
                        cryptocurrency.price_change_percentage_24h = price_change_percentage_24h
                        cryptocurrency.save()

                # Example: Extracting cryptocurrency names and symbols
                filtered_data = [{'id': currency_detail['id'], 'image': currency_detail['image'], 'name': currency_detail['name'], 'symbol': currency_detail['symbol'], 'current_price': currency_detail['current_price'], 'high_24h': currency_detail['high_24h'], 'low_24h': currency_detail['low_24h'], 'price_change_24h': price_change_24h, 'price_change_percentage_24h': price_change_percentage_24h} for currency_detail in response_json]
                # For Drf
                # return Response(filtered_data, status=status.HTTP_200_OK)

                # For Html
                context = {
                    'search_currencies': filtered_data,
                }
                return render(request, 'crypto_currency.html', context)
            else:
                error_message = f'Failed to fetch data from CoinGecko API'
                return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except requests.exceptions.RequestException as e:
            error_message = f'Failed to fetch data: {e}'
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

