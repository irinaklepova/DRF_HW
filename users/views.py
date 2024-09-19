from django.shortcuts import render
from rest_framework import viewsets

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для модели пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
