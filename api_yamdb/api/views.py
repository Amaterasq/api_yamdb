from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from rest_framework import mixins

from reviews.models import Review, Comments, Titles
from .serializers import ReviewSerializer, CommentsSerializer
# from .permissions import IsOwnerOrReadOnly


class TitleViewSet(viewsets.ModelViewSet):
    pass


class CommentsViewSet(viewsets.ModelViewSet):
    """Отбираем только нужные комментарии к отзыву"""
    serializer_class = CommentsSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs.get('review_id'))
        )


class ReviewViewSet(viewsets.ModelViewSet):
    """Отбираем только нужные отзывы к произведению"""
    serializer_class = ReviewSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        )
