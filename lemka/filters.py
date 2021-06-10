import coreapi
from django.db.models import Q
from django_filters import rest_framework as df_filters
from rest_framework.filters import BaseFilterBackend

from lemka.models import Article, Mercerie


class GlobalArticleFilter(df_filters.FilterSet):
    search = df_filters.CharFilter(method='search_query', label='Search')
    # TODO - Compléter la recherche rayon section typeproduit

    class Meta:
        model = Article
        fields = [
            'ref_type_service',
            'ref_tags'
        ]

    def search_query(self, queryset, name, value):
        return queryset.filter(Q(titre__icontains=value) | Q(description__icontains=value))


class GlobalMercerieFilter(df_filters.FilterSet):
    search = df_filters.Filter(method='search_query', label='Search')

    class Meta:
        model = Mercerie
        fields = [
            'ref_categorie',
            'ref_couleur'
        ]

    def search_query(self, queryset, name, value):
        return queryset.filter(Q(reference__icontains=value) | Q(description__icontains=value))


class GlobalArticleSimpleFilter(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='search',
                location='query',
                required=False,
                type='string',
            ),
            coreapi.Field(
                name='titre',
                location='query',
                required=False,
                type='string'
            ),
            coreapi.Field(
                name='rayon',
                location='query',
                required=False,
                type='string'
            )
        ]
