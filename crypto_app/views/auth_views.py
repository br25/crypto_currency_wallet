from decimal import Decimal
from django.shortcuts import render, redirect
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from crypto_auth.models import CustomUser
from crypto_auth.serializers import CustomUserSerializer, PasswordResetSerializer
from crypto_app.models import Referral
from crypto_app.common_utils import ReferralCodeGenerator
from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes



class UserSignup(ReferralCodeGenerator, APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = CustomUser.objects.all()
        serializer = CustomUserSerializer(queryset, many=True)
        # For Drf
        # return Response(serializer.data)
        # Render the signup form HTML template for GET requests
        return render(request, 'signup.html')

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])

            # referral code genarator
            referral_generator = ReferralCodeGenerator()
            referral_code = referral_generator.generate_referral_code()
            user.referral_code = referral_code
            user.save()

            # Check if the request includes a referrer code
            referrer_code = request.data.get('referrer_code')
            if referrer_code:
                try:
                    # Find the referrer user based on the referrer code
                    referrer = CustomUser.objects.get(referral_code=referrer_code)
                    
                    # Bonus amount
                    bonus_amount = Decimal('100.00')

                    # Create a Referral model entry for the referrer and referred user
                    Referral.objects.create(
                        referrer=referrer,
                        referred_user=user,
                        bonus_amount=bonus_amount,
                    )

                    # Add the bonus to the referrer's account
                    referrer.balance += bonus_amount
                    referrer.save()

                    # Add the bonus to the referred user's account
                    user.balance += bonus_amount
                    user.save()
                except CustomUser.DoesNotExist:
                    return Response({"message": "Invalid referrer code"}, status=status.HTTP_400_BAD_REQUEST)

            # DRF
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            # Redirect login
            return redirect('login')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLogin(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # queryset = CustomUser.objects.all()
        # serializer = CustomUserSerializer(queryset, many=True)
        # For Drf
        # return Response(serializer.data)
        # Render the signup form HTML template for GET requests
        return render(request, 'login.html')

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = CustomUser.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        serializer = CustomUserSerializer(user)
        # DRf
        # return Response(serializer.data)
        
        # Redirect crypto Home
        return redirect('crypto')



class UserLogout(APIView):
    def post(self, request):
        logout(request)
        return redirect('login')


class PasswordResetAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return render(request, 'password_reset.html')

    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not email or not new_password or not confirm_password:
            return Response({'error': 'Email, new password, and confirmation password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({'error': 'New password and confirmation password do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password for the user
        user.set_password(new_password)
        user.save()

        return redirect('login')
