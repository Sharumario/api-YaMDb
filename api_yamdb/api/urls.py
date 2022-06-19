from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import CommentViewSet, ReviewViewSet, UserViewSet, signup, token

router_v1 = SimpleRouter()
router_v1.register(r'users', UserViewSet, basename='user')
router_v1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review')
router_v1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', token),
    path('v1/', include(router_v1.urls)),
]
