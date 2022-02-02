from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import TitleViewSet, CommentsViewSet


router = DefaultRouter()
# router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'titles/?P<title_id>/reviews/?P<review_id>/comments',
                CommentsViewSet, basename='comments')
urlpatterns = [
    path('v1/', include(router.urls)),
]
