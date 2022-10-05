from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import api_home


urlpatterns = [
    path('auth/', obtain_auth_token),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # 엑세스 토큰을 실제로 얻기 위한 뷰
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # 토큰 새로고침 시 실제 엑세스 토큰을 확인
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), # JWT클라이언트가 실제 토큰인지 확인한다.
    path('', api_home),
]
