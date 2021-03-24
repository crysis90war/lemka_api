from datetime import datetime, timedelta

from django.db.models import Q
from rest_framework import generics, status, views
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from administrateur.serializers import ArticleSerializer
from lemka.models import (
    User, UserMensuration, MensurationUserMensuration, Adresse, DemandeDevis, Article, RendezVous, TypeService, Horaire
)
from lemka.permissions import UserGetPostPermission
# from lemka.serializers import *
from utilisateur.serializers import UserDemandeDevisSerializer, UserRendezVousSerializer, AdresseSerializer, ProfilSerializer, \
    UserMensurationSerializer, MensurationUserMensurationSerializer, UserAdresseSerializer


class ProfilAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfilSerializer

    # permission_classes = [IsAuthenticated, UserRUDPermission, ]

    # parser_classes = (MultiPartParser, FormParser,)

    def get_object(self):
        user_object = self.request.user
        return user_object

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer_context = {'request': request}
        serializer = self.serializer_class(user, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserMensurationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = UserMensurationSerializer
    permission_classes = [IsAuthenticated, UserGetPostPermission, ]

    def get_queryset(self):
        if self.request.user and not self.request.user.is_anonymous:
            queryset = UserMensuration.objects.filter(ref_user=self.request.user)
            return queryset
        else:
            raise ValidationError("Les utilisateurs anonymes ne disposent d'aucun droit !")

    def perform_create(self, serializer):
        if self.request.user and not self.request.user.is_anonymous:
            request_user = self.request.user
            user_mensurations = UserMensuration.objects.filter(ref_user=request_user)

            if user_mensurations.count() >= 5:
                raise ValidationError(
                    "Vous avez déja 5 mensurations enregistrés, Veuillez modifier ou supprimer pour ajouter un "
                    "nouveau !")

            serializer.save(ref_user=request_user)
        else:
            raise ValidationError("Les utilisateurs anonymes ne disposent d'aucun droit !")


class UserMensurationRUDApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserMensuration.objects.all()
    serializer_class = UserMensurationSerializer


class MensurationUserMensurationListApiView(generics.ListAPIView):
    queryset = MensurationUserMensuration.objects.all()
    serializer_class = MensurationUserMensurationSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        kwarg_user = self.request.user
        kwarg_id = self.kwargs.get('ref_user_mensuration_id')
        return MensurationUserMensuration.objects.filter(ref_user_mensuration=kwarg_id,
                                                         ref_user_mensuration__ref_user=kwarg_user)


class MensurationUserMensurationUpdateApiView(generics.RetrieveUpdateAPIView):
    queryset = MensurationUserMensuration.objects.all()
    serializer_class = MensurationUserMensurationSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        kwarg_ref_user_mensuration_id = self.kwargs.get('ref_user_mensuration_id')
        return MensurationUserMensuration.objects.filter(
            ref_user_mensuration_id=kwarg_ref_user_mensuration_id,
        )


class AdresseCreateAPIView(generics.CreateAPIView):
    serializer_class = UserAdresseSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        request_user = self.request.user

        if Adresse.objects.filter(ref_user=request_user).exists():
            raise ValidationError("Adresse existe déja !")

        serializer.save(ref_user=request_user)


class AdresseRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Adresse.objects.all()
    serializer_class = AdresseSerializer

    def get_object(self):
        adresse_object = get_object_or_404(Adresse, ref_user=self.request.user)
        return adresse_object

    def get(self, request, *args, **kwargs):
        adresse = self.get_object()
        serializer_context = {'request': request}
        serializer = self.serializer_class(adresse, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDemandeDevisListCreateApiView(generics.ListCreateAPIView):
    queryset = DemandeDevis.objects.all()
    serializer_class = UserDemandeDevisSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        request_user = self.request.user
        demandes_devis = DemandeDevis.objects.filter(ref_user=request_user)
        return demandes_devis

    def perform_create(self, serializer):
        request_user = self.request.user
        serializer.save(ref_user=request_user)


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


class RendezVousViewSet(generics.ListCreateAPIView):
    """
    TODO - url manquant
    """
    queryset = RendezVous.objects.all()
    lookup_field = "pk"
    serializer_class = UserRendezVousSerializer
    permission_classes = [IsAuthenticated, ]

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
