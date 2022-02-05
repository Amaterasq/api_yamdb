from rest_framework import viewsets, filters, mixins
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from api.serializers import (
    TitleSerializer, ReviewSerializer, CommentsSerializer, CategorySerializer
)
from reviews.models import Category, Genre, Title, Review
from api.filters import TitlesFilter


class TitleViewSet(viewsets.ModelViewSet):

    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenresViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = CategorySerializer
    queryset = Genre.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=self.kwargs.get('title_id'))
        )


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
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=self.kwargs.get('title_id'))
        )
