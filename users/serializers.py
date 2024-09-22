from rest_framework.serializers import ModelSerializer

from users.models import User, Payment


class PaymentSerializer(ModelSerializer):
    """Сериализатор для модели платежа"""

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    """Сериализатор для пользователя"""
    payment_history = PaymentSerializer(source='user', many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'city', 'avatar', 'payment_history',)


class OtherUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'last_name', 'payment_history']
