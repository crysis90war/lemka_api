import coreapi
from django_filters import rest_framework as df_filters
from rest_framework.filters import BaseFilterBackend

from lemka.models import Article


class GlobalArticleFilter(df_filters.FilterSet):
    titre = df_filters.CharFilter(lookup_expr='icontains')
    description = df_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Article
        fields = (
            'titre',
            'description',
            'ref_catalogue__ref_rayon',
            'ref_catalogue__ref_section',
            'ref_catalogue__ref_type_produit',
        )


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
