from django.urls import path
from users import api
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='api-login'),
    path('resfresh/', TokenRefreshView.as_view(), name='api-refresh-token'),
    path('forgot-password/', api.ForgotPasswordAPI.as_view(), name='api-forgot-password'),
    path('register/', api.UserCreateAPI.as_view(), name='api-register'),
    path('profile/', api.ProfileAPI.as_view(), name='api-user-profile'),
    path('all/', api.UserListAPI.as_view(), name='api-user-list'),
    path('<uuid>/', api.UserAPI.as_view(), name='api-single-user'),
    path('<uuid>/update', api.UserUpdateAPI.as_view(), name='api-update-user'),
    path('<uuid>/delete', api.UserUpdateAPI.as_view(), name='api-delete-user'),
    path('logout/blacklist/', api.BlacklistAPI.as_view(), name='api-blacklist'),
    path('activate/<uidb64>/<token>', api.ActiveAccountAPI.as_view(), name='api-activate'),
    path('reset-password/<uidb64>/<token>/', api.ResetPasswordAPI.as_view(), name='api-confirm-reset-password'),
]