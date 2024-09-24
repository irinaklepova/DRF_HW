from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsOwner, IsStaff
from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer, OtherUserSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели платежа"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course_pay', 'lesson_pay', 'method',)
    ordering_fields = ('payment_day',)

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product_id = create_stripe_product(payment)
        price = create_stripe_price(payment.amount, product_id)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class UsersCreateAPIView(CreateAPIView):
    """Generic-класс для создания пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListView(ListAPIView):
    """Generic-класс для вывода списка пользователей"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)


class UserDetailPIView(RetrieveAPIView):
    """Generic-класс для просмотра одного пользователя"""
    # serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.user == self.get_object():
            self.serializer_class = UserSerializer
        else:
            self.serializer_class = OtherUserSerializer
        return self.serializer_class


class UserUpdateAPIView(UpdateAPIView):
    """Generic-класс для редактирования пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class UserDeleteAPIView(DestroyAPIView):
    """Generic-класс для удаления пользователя"""
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsOwner, ~IsStaff,)
