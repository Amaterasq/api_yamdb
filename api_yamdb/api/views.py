from rest_framework import viewsets, filters, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import LimitOffsetPagination

from django.shortcuts import get_object_or_404

# from .permissions import IsOwnerOrReadOnly
from api.serializers import TitleSerializer, ReviewSerializer, CommentsSerializer
from reviews.models import Titles, Review, Comments


class TitleViewSet(viewsets.ModelViewSet):

    serializer_class = TitleSerializer
    queryset = Titles.objects.all()


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
