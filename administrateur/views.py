from rest_framework import viewsets, generics, filters
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from administrateur.pagination import SmallSetPagination
from lemka.permissions import IsAdminOrReadOnly
from lemka.serializers import *


class CommonFields(viewsets.ModelViewSet):
    lookup_field = 'pk'
    permission_classes = [IsAdminUser, ]


class PaysViewSet(viewsets.ModelViewSet):
    queryset = Pays.objects.all().order_by("pays")
    serializer_class = PaysSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class VilleViewSet(viewsets.ModelViewSet):
    queryset = Ville.objects.all().order_by("ref_pays__pays", "code_postale")
    serializer_class = VilleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['ville', 'code_postale']
    pagination_class = SmallSetPagination
    permission_classes = [IsAdminOrReadOnly, ]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by("genre")
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class TypeServiceViewSet(CommonFields):
    queryset = TypeService.objects.all().order_by("type_service")
    serializer_class = TypeServiceSerializer


class RayonViewSet(CommonFields):
    queryset = Rayon.objects.all().order_by("rayon")
    serializer_class = RayonSerializer


class SectionViewSet(CommonFields):
    queryset = Section.objects.all().order_by("section")
    serializer_class = SectionSerializer


class TypeProduitViewSet(CommonFields):
    queryset = TypeProduit.objects.all().order_by("type_produit")
    serializer_class = TypeProduitSerializer


class CatalogueViewSet(viewsets.ModelViewSet):
    queryset = Catalogue.objects.all().order_by("ref_rayon", "ref_section", "ref_type_produit")
    serializer_class = CatalogueSerializer
    permission_classes = [IsAdminUser, ]

    def perform_create(self, serializer):
        kwarg_rayon = serializer.validated_data['ref_rayon']
        kwarg_section = serializer.validated_data['ref_section']
        kwarg_type_produit = serializer.validated_data['ref_type_produit']

        if Catalogue.objects.filter(ref_rayon=kwarg_rayon, ref_section=kwarg_section,
                                    ref_type_produit=kwarg_type_produit).exists():
            raise ValidationError("Ce catalogue existe déja !")
        serializer.save(ref_rayon=kwarg_rayon, ref_section=kwarg_section, ref_type_produit=kwarg_type_produit)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by("tag")
    serializer_class = TagSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['tag']
    pagination_class = SmallSetPagination


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly, ]


class ArticleImageListCreateAPIView(generics.ListCreateAPIView):
    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageSerializer
    permission_classes = [IsAdminOrReadOnly, ]

    def get_queryset(self):
        """
        Permet de récupérer les images pour un article spécifique par slug
        :return: Retourne les images d'un article
        """
        kwarg_slug = self.kwargs.get("slug")
        test = ArticleImage.objects.filter(ref_article__slug=kwarg_slug)
        return test

    def perform_create(self, serializer):
        kwarg_slug = self.kwargs.get("slug")
        article = get_object_or_404(Article, slug=kwarg_slug)
        serializer.save(ref_article=article)


class ArticleImageRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class EntrepriseLemkaViewSet(viewsets.ModelViewSet):
    queryset = EntrepriseLemka.objects.all()
    serializer_class = EntrepriseLemkaSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer


class AccompteDemandeViewSet(viewsets.ModelViewSet):
    queryset = AccompteDemande.objects.all()
    serializer_class = AccompteDemandeSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminUser, ]


class CouleurViewSet(CommonFields):
    queryset = Couleur.objects.all()
    serializer_class = CouleurSerializer


class CategorieViewSet(CommonFields):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer


class MercerieViewSet(CommonFields):
    queryset = Mercerie.objects.all()
    serializer_class = MercerieSerializer


class MercerieCouleurViewSet(CommonFields):
    queryset = MercerieOption.objects.all()
    serializer_class = MercerieCouleurSerializer


class HoraireViewSet(CommonFields):
    queryset = Horaire.objects.all()
    serializer_class = HoraireSerializer


class DetailViewSet(CommonFields):
    queryset = Detail.objects.all()
    serializer_class = DetailSerialiser


class TvaViewSet(CommonFields):
    queryset = Tva.objects.all()
    serializer_class = TvaSertializer


class MensurationViewSet(viewsets.ModelViewSet):
    queryset = Mensuration.objects.all()
    serializer_class = MensurationSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class DetailListAPIView(generics.ListAPIView):
    serializer_class = DetailSerialiser

    def get_queryset(self):
        kwarg_devis = self.kwargs.get('numero_devis')
        devis = Detail.objects.filter(ref_devis__numero_devis=kwarg_devis)
        return devis


class DetailCreateAPIView(generics.CreateAPIView):
    queryset = Detail.objects.all()
    serializer_class = DetailSerialiser
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        kwarg_devis = self.kwargs.get("numero_devis")
        devis = get_object_or_404(Devis, numero_devis=kwarg_devis)
        serializer.save(ref_devis=devis)


class DetailRUDApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Detail.objects.all()
    serializer_class = DetailSerialiser
    permission_classes = [IsAdminUser]

    # def get_queryset(self):
    #     kwarg_id = self.kwargs.get('pk')
    #     kwarg_devis = self.kwargs.get('numero_devis')
    #     devis = Detail.objects.filter(ref_devis__numero_devis=kwarg_devis, pk=kwarg_id)
    #     return devis

    def get_object(self):
        queryset = self.get_queryset()
        kwarg_devis = self.kwargs.get('numero_devis')
        kwarg_id = self.kwargs.get('pk')
        try:
            obj = get_object_or_404(queryset, ref_devis__numero_devis=kwarg_devis, pk=kwarg_id)
            return obj
        except Exception as e:
            raise ValidationError(e)


class MercerieCouleurImageListCreateAPIView(generics.ListCreateAPIView):
    queryset = MercerieOptionImage.objects.all()
    serializer_class = MercerieCouleurImageSerializer

    def get_queryset(self):
        kwarg_pk = self.kwargs.get("pk")
        merceriescouleur = MercerieOptionImage.objects.filter(ref_mercerie_option_id=kwarg_pk)
        return merceriescouleur

    def perform_create(self, serializer):
        kwarg_pk = self.kwargs.get("pk")
        mercerie = get_object_or_404(MercerieOption, id=kwarg_pk)
        serializer.save(ref_mercerie_couleur=mercerie)


class MercerieCouleurImageRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MercerieOptionImage.objects.all()
    serializer_class = MercerieCouleurImageSerializer
    permission_classes = [IsAdminUser, ]


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]


class UserRetrieveAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"

    def get_object(self):
        queryset = self.get_queryset()
        kwarg_username = self.kwargs.get("username")
        obj = get_object_or_404(queryset, username=kwarg_username)
        return obj


class UserAdresseRUDApiView(generics.RetrieveUpdateAPIView):
    queryset = Adresse.objects.all()
    serializer_class = AdresseSerializer

    def get_object(self):
        queryset = self.get_queryset()
        kwarg_username = self.kwargs.get("username")
        obj = get_object_or_404(queryset, ref_user__username=kwarg_username)
        return obj


class CheckUserAPIView(APIView):

    def get(self, request, *args, **kwargs):
        message = 'message'
        if self.request.user.is_anonymous:
            return Response(data={message: 'Veuillez vous connecter '})
        elif self.request.user.is_staff:
            username = self.kwargs.get('username')
            if User.objects.filter(username=username).exists():
                return Response(data={message: True})
            else:
                return Response(data={message: False})
        else:
            return Response(data={message: 'Admins only allowed'})


class Dashboard(APIView):

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_anonymous and self.request.user.is_staff:
            users_count = User.objects.count()
            articles_counts = Article.objects.count()
            merceries_count = Mercerie.objects.count()
            demandes_de_devis_count = DemandeDevis.objects.count()
            devis_count = Devis.objects.count()
            bons_de_commande_count = BonCommande.objects.count()
            factures_count = Facture.objects.count()
            rendez_vous_count = RendezVous.objects.count()

            admin_dashboard = {
                'user_count': users_count,
                'articles_count': articles_counts,
                'merceries_count': merceries_count,
                'demandes_de_devis_count': demandes_de_devis_count,
                'devis_count': devis_count,
                'bons_de_commande_count': bons_de_commande_count,
                'factures_count': factures_count,
                'rendez_vous_count': rendez_vous_count,
            }

            return Response(data=admin_dashboard)
        else:
            raise ValidationError('Vous n\'avez pas l\'autorisation')
