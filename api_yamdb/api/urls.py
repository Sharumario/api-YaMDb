from django.urls import include, path

from rest_framework import routers

router_v1 = routers.SimpleRouter()

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
