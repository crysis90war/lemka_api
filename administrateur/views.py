from rest_framework import viewsets, generics, filters, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from administrateur.serializers import (
    GenreSerializer, VilleSerializer, PaysSerializer, EntrepriseLemkaSerializer, UserSerializer, AdminDemandeDevisSerializer, AdminDevisSerializer,
    TagSerializer, TypeServiceSerializer, AdminAdresseSerializer, CaracteristiqueSerializer, RayonSerializer, SectionSerializer,
    TypeProduitSerializer, CatalogueSerializer, CouleurSerializer, CategorieSerializer, HoraireSerializer, DetailSerialiser, TvaSertializer,
    MensurationSerializer, ArticleSerializer, ArticleImageSerializer, MercerieImageSerializer,
    MercerieCaracteristiqueSerializer, MercerieSerializer, AdminRendezVousSerializer
)
from lemka.models import (
    Pays, Ville, Caracteristique, Genre, TypeService, Rayon, Section, TypeProduit, Catalogue, User, Article, Mercerie, DemandeDevis, Devis,
    RendezVous, Tag, Couleur, Categorie, Entreprise, Horaire, Detail, Tva, Mensuration, ArticleImage, Adresse, MercerieCaracteristique,
    MercerieImage, UserMensuration
)
from lemka.pagination import SmallSetPagination
from lemka.permissions import IsAdminOrReadOnly
from utilisateur.serializers import UserMensurationSerializer


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


class CaracteristiqueViewSet(viewsets.ModelViewSet):
    queryset = Caracteristique.objects.all()
    serializer_class = CaracteristiqueSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by("nom")
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class TypeServiceViewSet(viewsets.ModelViewSet):
    queryset = TypeService.objects.all().order_by("nom")
    serializer_class = TypeServiceSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class RayonViewSet(viewsets.ModelViewSet):
    queryset = Rayon.objects.all().order_by("nom")
    serializer_class = RayonSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all().order_by("nom")
    serializer_class = SectionSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class TypeProduitViewSet(viewsets.ModelViewSet):
    queryset = TypeProduit.objects.all().order_by("nom")
    serializer_class = TypeProduitSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class CatalogueViewSet(viewsets.ModelViewSet):
    queryset = Catalogue.objects.all().order_by("ref_rayon", "ref_section", "ref_type_produit")
    serializer_class = CatalogueSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['ref_rayon__rayon', 'ref_section__section', 'ref_type_produit__type_produit']
    permission_classes = [IsAdminOrReadOnly, ]

    def perform_create(self, serializer):
        kwarg_rayon = serializer.validated_data['ref_rayon']
        kwarg_section = serializer.validated_data['ref_section']
        kwarg_type_produit = serializer.validated_data['ref_type_produit']

        if Catalogue.objects.filter(ref_rayon=kwarg_rayon, ref_section=kwarg_section, ref_type_produit=kwarg_type_produit).exists():
            raise ValidationError(detail={"detail": "Ce catalogue existe déja !"})
        serializer.save(ref_rayon=kwarg_rayon, ref_section=kwarg_section, ref_type_produit=kwarg_type_produit)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by("nom")
    serializer_class = TagSerializer
    lookup_field = 'pk'
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom']
    pagination_class = SmallSetPagination
    permission_classes = [IsAdminOrReadOnly, ]


class CouleurViewSet(viewsets.ModelViewSet):
    queryset = Couleur.objects.all()
    serializer_class = CouleurSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminOrReadOnly, ]


class DevisViewSet(viewsets.ModelViewSet):
    queryset = Devis.objects.all()
    serializer_class = AdminDevisSerializer
    permission_classes = [IsAdminUser, ]

    def perform_create(self, serializer):
        kwarg_demande_devis = serializer.validated_data['ref_demande_devis']

        if Devis.objects.filter(ref_demande_devis=kwarg_demande_devis).exists():
            raise ValidationError(
                detail={"detail": "Il y a deja un devis pour cette demande, veuillez modifier l'existant !"},
                code=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(ref_demande_devis=kwarg_demande_devis)


class EntrepriseLemkaViewSet(viewsets.ModelViewSet):
    queryset = Entreprise.objects.all()
    serializer_class = EntrepriseLemkaSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class HoraireViewSet(viewsets.ModelViewSet):
    queryset = Horaire.objects.all().order_by('jour_semaine')
    serializer_class = HoraireSerializer
    permission_classes = [IsAdminOrReadOnly]


class DetailViewSet(viewsets.ModelViewSet):
    queryset = Detail.objects.all()
    serializer_class = DetailSerialiser
    permission_classes = [IsAdminUser]


class TvaViewSet(viewsets.ModelViewSet):
    queryset = Tva.objects.all()
    serializer_class = TvaSertializer
    permission_classes = [IsAdminOrReadOnly]


class MensurationViewSet(viewsets.ModelViewSet):
    queryset = Mensuration.objects.all()
    serializer_class = MensurationSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class DetailsListCreateApiView(generics.ListCreateAPIView):
    queryset = Detail.objects.all()
    serializer_class = DetailSerialiser
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        kwarg_devis_id = self.kwargs.get('devis_id')
        devis = Detail.objects.filter(ref_devis__pk=kwarg_devis_id)
        return devis

    def perform_create(self, serializer):
        kwarg_devis_id = self.kwargs.get("devis_id")
        devis = get_object_or_404(Devis, pk=kwarg_devis_id)
        serializer.save(ref_devis=devis)


class DetailRUDApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Detail.objects.all()
    serializer_class = DetailSerialiser
    permission_classes = [IsAdminUser]

    def get_object(self):
        queryset = self.get_queryset()
        kwarg_devis = self.kwargs.get('devis_id')
        kwarg_id = self.kwargs.get('pk')
        try:
            obj = get_object_or_404(queryset, ref_devis__pk=kwarg_devis, pk=kwarg_id)
            return obj
        except Exception as e:
            raise ValidationError(e)


# region Traitement Article
class ArticleListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        if not self.request.user.is_staff:
            queryset = Article.objects.filter(est_active=True).order_by('-created_at')
            return queryset
        else:
            queryset = Article.objects.all().order_by('-created_at')
            return queryset


class ArticleRUDApiView(generics.RetrieveUpdateDestroyAPIView):
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

# endregion


# region Traitement Mercerie

class MercerieListCreateApiView(generics.ListCreateAPIView):
    queryset = Mercerie.objects.all()
    serializer_class = MercerieSerializer
    permission_classes = [IsAdminUser]


class MercerieRUDApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mercerie.objects.all()
    serializer_class = MercerieSerializer
    permission_classes = [IsAdminUser]


class MercerieImageCreateApiView(generics.CreateAPIView):
    queryset = MercerieImage.objects.all()
    serializer_class = MercerieImageSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        kwarg_mercerie_id = self.kwargs.get('mercerie_id')
        mercerie = get_object_or_404(Mercerie, pk=kwarg_mercerie_id)
        serializer.save(ref_mercerie=mercerie)


class MercerieImageDestroyAPIView(generics.DestroyAPIView):
    queryset = MercerieImage.objects.all()
    serializer_class = MercerieImageSerializer
    permission_classes = [IsAdminUser]


class MercerieCaracteristiqueCreateApiView(generics.CreateAPIView):
    queryset = MercerieCaracteristique
    serializer_class = MercerieCaracteristiqueSerializer
    permission_classes = [IsAdminUser, ]

    def perform_create(self, serializer):
        kwarg_mercerie_id = self.kwargs.get('mercerie_id')
        mercerie = get_object_or_404(Mercerie, pk=kwarg_mercerie_id)
        serializer.save(ref_mercerie=mercerie)


class MercerieCaracteristiqueRUDApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MercerieCaracteristique.objects.all()
    serializer_class = MercerieCaracteristiqueSerializer
    permission_classes = [IsAdminUser, ]

# endregion


# region Traitement de l'utilisateur

class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return User.objects.filter(is_superuser=False)


class UserRetrieveAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    permission_classes = [IsAdminUser]

    def get_object(self):
        queryset = self.get_queryset()
        kwarg_username = self.kwargs.get("username")
        obj = get_object_or_404(queryset, username=kwarg_username)
        return obj


class UserAdresseRUDApiView(generics.RetrieveUpdateAPIView):
    queryset = Adresse.objects.all()
    serializer_class = AdminAdresseSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        queryset = self.get_queryset()
        kwarg_username = self.kwargs.get("username")
        obj = get_object_or_404(queryset, ref_user__username=kwarg_username)
        return obj


class UserMensurationsListApiView(generics.ListAPIView):
    queryset = UserMensuration.objects.all()
    serializer_class = UserMensurationSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        kwarg_username = self.kwargs.get('username')
        queryset = UserMensuration.objects.filter(ref_user__username=kwarg_username).order_by('-is_main')
        return queryset

# endregion


class DemandeDevisViewSet(viewsets.ModelViewSet):
    queryset = DemandeDevis.objects.all().filter(est_soumis=True)
    lookup_field = "pk"
    serializer_class = AdminDemandeDevisSerializer
    permission_classes = [IsAdminUser]


class RendezVousViewSet(viewsets.ModelViewSet):
    queryset = RendezVous.objects.all()
    lookup_field = "pk"
    serializer_class = AdminRendezVousSerializer
    permission_classes = [IsAdminUser]


class CheckUserAPIView(APIView):
    permission_classes = [IsAdminUser]

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


class IsAdmin(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response(data={'detail': 'Welcome'})
