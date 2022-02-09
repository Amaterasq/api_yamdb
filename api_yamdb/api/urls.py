from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (
    TitleViewSet, CommentsViewSet, CategoryViewSet, GenresViewSet,
    ReviewViewSet
)
from .views import (
    send_confirmation_code,
    get_jwt_token,
    UsersViewSet,
    UserDetailPach
)

router = DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments'
)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenresViewSet, basename='genres')

urlpatterns = [
    path('v1/auth/signup/', send_confirmation_code),
    path('v1/auth/token/', get_jwt_token),
    path('v1/users/me/', UserDetailPach.as_view()),
    path('v1/', include(router.urls)),
]
