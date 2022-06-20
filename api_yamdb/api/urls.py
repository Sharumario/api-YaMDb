from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import CommentViewSet, CategoriesViewSet, GenreViewSet, ReviewViewSet, TitleViewSet, UserViewSet, signup, token

router_v1 = SimpleRouter()
router_v1.register(r'users', UserViewSet, basename='user')

router_v1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review')
router_v1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
router_v1.register(r'categories', CategoriesViewSet,
                   basename='category')
router_v1.register(r'genres', GenreViewSet, basename='genre')
router_v1.register(r'titles', TitleViewSet, basename='title')

urlpatterns = [
    path('auth/signup/', signup),
    path('auth/token/', token),
    path('', include(router_v1.urls)),
]
