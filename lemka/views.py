from rest_framework import generics, filters
from rest_framework.permissions import AllowAny

from administrateur.serializers import ArticleSerializer
from lemka.models import Article, Mercerie
from lemka.serializers import GlobalMercerieSerializer


class ArticleServiceListAPIView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        kwarg_type_service = self.kwargs.get("pk")
        return Article.objects.filter(ref_type_service__id=kwarg_type_service, est_active=True)


class ArticleRayonListAPIView(ArticleServiceListAPIView):

    def get_queryset(self):
        kwarg_rayon_slug = self.kwargs.get("rayon_slug")
        return Article.objects.filter(ref_catalogue__ref_rayon__rayon_slug=kwarg_rayon_slug)


class ArticleSectionListAPIView(ArticleServiceListAPIView):

    def get_queryset(self):
        kwarg_rayon_slug = self.kwargs.get("rayon_slug")
        kwarg_section_slug = self.kwargs.get("section_slug")
        return Article.objects.filter(
            ref_catalogue__ref_rayon__rayon_slug=kwarg_rayon_slug,
            ref_catalogue__ref_section__section_slug=kwarg_section_slug
        )


class ArticleTypeProduitListAPIView(ArticleServiceListAPIView):

    def get_queryset(self):
        kwarg_rayon_slug = self.kwargs.get("rayon_slug")
        kwarg_section_slug = self.kwargs.get("section_slug")
        kwarg_type_produit_slug = self.kwargs.get("type_produit_slug")
        return Article.objects.filter(
            ref_catalogue__ref_rayon__rayon_slug=kwarg_rayon_slug,
            ref_catalogue__ref_section__section_slug=kwarg_section_slug,
            ref_catalogue__ref_type_produit__type_produit_slug=kwarg_type_produit_slug
        )


class GlobalMercerieListApiView(generics.ListAPIView):
    queryset = Mercerie.objects.all().filter(est_publie=True)
    serializer_class = GlobalMercerieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['reference', 'description', 'nom', 'ref_couleur__nom', 'ref_categorie__nom']
