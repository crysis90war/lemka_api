from datetime import datetime, timedelta

from django.db.models import Q
from rest_framework import viewsets, generics, views, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from lemka.serializers import *


# region Global

class HoraireListAPIView(generics.ListAPIView):
    queryset = Horaire.objects.all()
    serializer_class = HoraireSerializer
    permission_classes = [AllowAny, ]


class ArticleServiceListAPIView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        kwarg_type_service = self.kwargs.get("pk")
        return Article.objects.filter(ref_type_service__id=kwarg_type_service)


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


# endregion

# region Utilisateur

class ArticleLikeAPIView(views.APIView):
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]

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


class DemandeDevisViewSet(viewsets.ModelViewSet):
    queryset = DemandeDevis.objects.all()
    lookup_field = "pk"
    serializer_class = DemandeDevisSerializer

    def perform_create(self, serializer):
        serializer.save(ref_user=self.request.user)


class DevisViewSet(viewsets.ModelViewSet):
    queryset = Devis.objects.all()
    lookup_field = "numero_devis"
    serializer_class = DevisSerializer


class RendezVousViewSet(viewsets.ModelViewSet):
    queryset = RendezVous.objects.all()
    lookup_field = "pk"
    serializer_class = RendezVousSerializer

    def perform_create(self, serializer):
        request_user = self.request.user
        kwarg_date = datetime.strptime(str(serializer.validated_data["date"]), "%Y-%m-%d").date()
        now = datetime.now().date()
        start = serializer.validated_data["start"]
        ref_type_service = serializer.validated_data["ref_type_service"]
        type_service = TypeService.objects.get(pk=ref_type_service.id)
        result = datetime.strptime(str(start), "%H:%M:%S") + timedelta(minutes=type_service.duree_minute)
        end_time = result.time()
        day = datetime.strptime(str(kwarg_date), "%Y-%m-%d").weekday()
        horaire = Horaire.objects.get(jour_semaine=day)
        if kwarg_date < now:
            raise ValidationError("La date choisie ne peut pas être inférieur a celle d'aujourd'hui !")
        elif RendezVous.objects.filter(date=kwarg_date).filter(
                (Q(start__gte=start) & Q(start__lte=end_time) | Q(end__gte=start))):
            raise ValidationError("Il y a déja une réservation pour ce jour, veillez choisir un autre moment !")
        elif kwarg_date == now:
            raise ValidationError("Le rendez-vous n'est pas possible pour le jour même !")
        elif horaire.sur_rdv is False and horaire.est_ferme is False:
            raise ValidationError("Nous sommes ouvert ce jour sans rendez-vous, veillez choisir un autre jour !")
        elif horaire.est_ferme:
            raise ValidationError("C'est fermé ce jour, choisisez un autre jour !")
        # TODO - Compléter le test sur une réservation de rendez-vous
        elif horaire.sur_rdv is True & (start < horaire.heure_ouverture or end_time > horaire.heure_fermeture):
            ouvert = horaire.heure_ouverture
            ferme = horaire.heure_fermeture
            pause_debut = horaire.pause_debut
            pause_fin = horaire.payse_fin
            raise ValidationError(f'Veuillez choisir une heure de {ouvert} à {pause_debut} et de {pause_fin} à {ferme}')
        else:
            serializer.save(ref_user=request_user, end=end_time)

# endregion
