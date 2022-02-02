from rest_framework import viewsets

from api.serializers import TitleSerializer
from reviews.models import Titles


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Titles.objects.all()
