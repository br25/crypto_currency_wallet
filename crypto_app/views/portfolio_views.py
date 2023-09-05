from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from crypto_auth.models import CustomUser
from ..models import CryptoCurrency, Portfolio, Referral
from ..serializers import PortfolioSerializer, ReferralSerializer
from crypto_auth.serializers import CustomUserSerializer

class PortfolioView(APIView):
    def get(self, request):
        # My Wallet
        wallet = CustomUser.objects.filter(email=request.user.email)
        wallet_serializer = CustomUserSerializer(wallet, many=True)

        # Cryptocurrency
        cryptocurrency = Portfolio.objects.filter(user=request.user)
        cryptocurrency_serializer = PortfolioSerializer(cryptocurrency, many=True)
        
        # Referral
        referrals = Referral.objects.filter(referrer=request.user)
        referrals_serializer = ReferralSerializer(referrals, many=True)
        
        context = {
            'wallet_data': wallet_serializer.data,
            'portfolio_data': cryptocurrency_serializer.data,
            'referral_data': referrals_serializer.data,
        }

        # # DRF
        # return Response(wallet_serializer.data)
        
        # Render portfolio with both portfolio_data and referral_data
        return render(request, 'portfolio.html', context)

    def post(self, request):
        currency_id = request.data.get('currency_id')
        
        try:
            # Retrieve the cryptocurrency by its unique identifier (e.g., 'id' field)
            cryptocurrency = CryptoCurrency.objects.get(id=currency_id)

            # Check if the user already has this cryptocurrency in their portfolio
            existing_portfolio = Portfolio.objects.filter(user=request.user, cryptocurrency=cryptocurrency).first()

            if existing_portfolio:
                # If it exists, update the quantity (increase by 1 in this example)
                existing_portfolio.quantity += 1
                existing_portfolio.save()
            else:
                # If it doesn't exist, create a new portfolio entry with quantity 1
                portfolio = Portfolio.objects.create(user=request.user, cryptocurrency=cryptocurrency, quantity=1)

            # Serialize the updated portfolio data
            portfolios = Portfolio.objects.filter(user=request.user)
            serializer = PortfolioSerializer(portfolios, many=True)
            # Drf
            # return Response(serializer.data, status=status.HTTP_200_OK)
            # html redirect
            return redirect('add-to-portfolio')

        except CryptoCurrency.DoesNotExist:
            return Response({'error': 'Cryptocurrency not found in the database'}, status=status.HTTP_404_NOT_FOUND)


class ReferralView(APIView):
    def get(self, request):
        referrals = Referral.objects.filter(referrer=request.user)
        serializer = ReferralSerializer(referrals, many=True)
        
        # DRF
        # return Response(serializer.data)
        # render portfolio
        return render(request, 'portfolio.html', {'referral_data': serializer.data})


class RemoveCryptoCurrencyView(APIView):
    def post(self, request, currency_id):
        # Find the specific portfolio item with the given currency_id
        portfolio_item = get_object_or_404(Portfolio, user=request.user, cryptocurrency__id=currency_id)

        # Decrement the quantity by 1 if it's greater than 0
        if portfolio_item.quantity > 0:
            portfolio_item.quantity -= 1

            # If quantity becomes 0, remove the portfolio item
            if portfolio_item.quantity == 0:
                portfolio_item.delete()
            else:
                portfolio_item.save()
        else:
            # Handle the case where the quantity is already 0
            messages.error(request, 'Cannot remove cryptocurrency. Quantity is already 0.')

        # Redirect back to the portfolio page
        return redirect('add-to-portfolio')