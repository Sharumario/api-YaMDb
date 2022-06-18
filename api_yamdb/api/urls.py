from django.urls import include, path

from rest_framework import routers

from .views import UserViewSet, signup, token
from .views import CategoriesViewSet

router_v1 = routers.SimpleRouter()
router_v1.register(r'users', UserViewSet, basename='user')
router_v1.register(r'^categories/(?P<slug>[-\w]+)/$', CategoriesViewSet, # ебусь с этим
                   basename='category')

urlpatterns = [
    path('auth/signup/', signup),
    path('auth/token/', token),
    path('', include(router_v1.urls)),
]
