from rest_framework import serializers
from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True, source='payment_set')

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'payments']
