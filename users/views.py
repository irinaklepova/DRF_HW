from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsOwner, IsStaff
from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer, OtherUserSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели пользователя"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course_pay', 'lesson_pay', 'method',)
    ordering_fields = ('payment_day',)


class UsersCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)


class UserDetailPIView(RetrieveAPIView):
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
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsOwner, ~IsStaff,)
