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

router_v1 = DefaultRouter()
router_v1.register(r'users', UsersViewSet, basename='users')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments'
)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenresViewSet, basename='genres')

urlpatterns = [
    path('v1/auth/signup/', send_confirmation_code),
    path('v1/auth/token/', get_jwt_token),
    path('v1/users/me/', UserDetailPach.as_view()),
    path('v1/', include(router_v1.urls)),
]
