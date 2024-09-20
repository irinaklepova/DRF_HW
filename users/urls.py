from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentViewSet, UsersCreateAPIView, UserListView, UserDetailPIView, \
    UserUpdateAPIView, UserDeleteAPIView

app_name = UsersConfig.name

router = DefaultRouter()
# router.register(r'users', UserViewSet, basename='users')
router.register(r'payments', PaymentViewSet, basename='payments')
urlpatterns = [
                  path('register/', UsersCreateAPIView.as_view(), name='register'),
                  path('users_list/', UserListView.as_view(), name='users_list'),
                  path('users/<int:pk>/', UserDetailPIView.as_view(), name='users_detail'),
                  path('users/update/<int:pk>/', UserUpdateAPIView.as_view(), name='users_update'),
                  path('users/delete/<int:pk>/', UserDeleteAPIView.as_view(), name='users_delete'),

                  path('token/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='token'),
                  path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)),
                       name='token_refresh'),
              ] + router.urls
