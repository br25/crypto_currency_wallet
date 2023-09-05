from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'referral_code', 'balance', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }



class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    