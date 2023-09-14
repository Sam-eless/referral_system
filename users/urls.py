from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserCreateView, UserAuthUpdateView, UserDetailView, UserListView, UserUpdateView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', UserListView.as_view(), name="user_list"),
    path('<int:pk>/', UserDetailView.as_view(), name="user_detail"),
    path('user-create/', UserCreateView.as_view(), name='create_user'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name="update_user"),
    path('auth-user/', UserAuthUpdateView.as_view(), name="auth_user"),
]
