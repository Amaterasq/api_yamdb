from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import TitleViewSet


router = DefaultRouter()
router.register(r'titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
]
