from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..models import CryptoCurrency, Portfolio, Referral
from ..serializers import PortfolioSerializer, ReferralSerializer

# @permission_classes([IsAuthenticated])
class PortfolioView(APIView):
    def get(self, request):
        portfolios = Portfolio.objects.filter(user=request.user)
        serializer = PortfolioSerializer(portfolios, many=True)
        # return Response(serializer.data)
        return render(request, 'portfolio.html', {'portfolio_data': serializer.data})

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


# # @permission_classes([IsAuthenticated])
# class ReferralView(APIView):
#     def get(self, request):
#         referrals = Referral.objects.filter(referrer=request.user)
#         serializer = ReferralSerializer(referrals, many=True)
#         # return Response(serializer.data)
#         return render(request, 'portfolio.html', {'referral_data': serializer.data})

#     def post(self, request):
#         serializer = ReferralSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(referrer=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
