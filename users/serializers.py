from rest_framework.serializers import ModelSerializer

from users.models import User, Payment


class UserSerializer(ModelSerializer):
    """Сериализатор для пользователя"""

    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'password', 'is_active', 'is_staff', 'is_superuser',)


class PaymentSerializer(ModelSerializer):
    """Сериализатор для модели платежа"""

    class Meta:
        model = Payment
        fields = "__all__"
