from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import TitleViewSet, CommentsViewSet, ReviewViewSet


router = DefaultRouter()
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                CommentsViewSet, basename='comments')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
urlpatterns = [
    path('v1/', include(router.urls)),
]
