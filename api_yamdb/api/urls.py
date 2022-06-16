from django.urls import include, path
from rest_framework import routers

from api.views import UserViewSet, signup, token

router_v1 = routers.SimpleRouter()
router_v1.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', token),
    path('v1/', include(router_v1.urls)),
]
