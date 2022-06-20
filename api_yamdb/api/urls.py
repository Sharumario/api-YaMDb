from django.urls import include, path

from rest_framework import routers

from .views import UserViewSet, signup, token
from .views import CategoriesViewSet, GenreViewSet, TitleViewSet

router_v1 = routers.SimpleRouter()
router_v1.register(r'users', UserViewSet, basename='user')
router_v1.register(r'categories', CategoriesViewSet,
                   basename='category')
router_v1.register(r'genres', GenreViewSet, basename='genre')
router_v1.register(r'titles', TitleViewSet, basename='title')

urlpatterns = [
    path('auth/signup/', signup),
    path('auth/token/', token),
    path('', include(router_v1.urls)),
]
