from django.shortcuts import render
from rest_framework import viewsets

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для модели пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели пользователя"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
