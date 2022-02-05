import django_filters

from reviews.models import Titles


class TitlesFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name='category__slug', lookup_expr='icontains'
    )
    genre = django_filters.CharFilter(
        field_name='genre__slug', lookup_expr='icontains'
    )
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains'
    )

    class Meta():
        model = Titles
        fields = ('category', 'genre', 'name', 'year')
