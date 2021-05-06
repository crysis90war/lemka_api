from rest_framework.response import Response
from rest_framework import generics, filters, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from administrateur.serializers import ArticleSerializer
from lemka.models import Article, Mercerie
from lemka.serializers import GlobalMercerieSerializer, GlobalArticleSerializer


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


class GlobalArticlesListApiView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = GlobalArticleSerializer

    def get_queryset(self):
        query = self.queryset.filter(est_active=True)

        return query


class ArticleLikeAPIView(APIView):
    serializer_class = GlobalArticleSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        user = request.user
        article.likes.remove(user)
        article.save()

        serializer_context = {'request': request}
        serializer = self.serializer_class(article, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        user = request.user
        article.likes.add(user)
        article.save()

        serializer_context = {'request': request}
        serializer = self.serializer_class(article, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)
