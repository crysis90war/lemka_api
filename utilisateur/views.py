from datetime import datetime, timedelta

from django.db.models import Q
from rest_framework import generics, status, views
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from administrateur.serializers import ArticleSerializer, AdminDevisSerializer, HoraireSerializer
from lemka.models import (
    User, UserMensuration, UserMensurationMesure, Adresse, DemandeDevis, Article, RendezVous, TypeService, Horaire, Devis
)
from lemka.permissions import UserGetPostPermission
from utilisateur.serializers import (
    UserDemandeDevisSerializer, UserRendezVousSerializer, AdresseSerializer, ProfilSerializer, UserMensurationSerializer,
    UserMensurationMesureSerializer, UserAdresseSerializer, UserDevisAccepterSerializer, RendezVousExistantSerializer
)


class ProfilAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfilSerializer
    permission_classes = [IsAuthenticated, ]

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


class UserMensurationMesureListApiView(generics.ListAPIView):
    queryset = UserMensurationMesure.objects.all()
    serializer_class = UserMensurationMesureSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        kwarg_user = self.request.user
        kwarg_id = self.kwargs.get('ref_user_mensuration_id')
        return UserMensurationMesure.objects.filter(ref_user_mensuration=kwarg_id, ref_user_mensuration__ref_user=kwarg_user)


class UserMensurationMesureRUApiView(generics.RetrieveUpdateAPIView):
    queryset = UserMensurationMesure.objects.all()
    serializer_class = UserMensurationMesureSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        kwarg_ref_user_mensuration_id = self.kwargs.get('ref_user_mensuration_id')
        return UserMensurationMesure.objects.filter(ref_user_mensuration_id=kwarg_ref_user_mensuration_id)


class AdresseCreateAPIView(generics.CreateAPIView):
    serializer_class = UserAdresseSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        request_user = self.request.user

        if Adresse.objects.filter(ref_user=request_user).exists():
            raise ValidationError(detail={"detail": "Vous avez déja une adresse !"})
        serializer.save(ref_user=request_user)


class AdresseRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Adresse.objects.all()
    serializer_class = AdresseSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        adresse_object = get_object_or_404(Adresse, ref_user=self.request.user)
        return adresse_object

    def get(self, request, *args, **kwargs):
        if Adresse.objects.filter(ref_user=self.request.user).exists():
            test = Adresse.objects.get(ref_user=self.request.user)
            serializer = self.serializer_class(test)
            return Response(serializer.data)
            # adresse = self.get_object()
            # serializer_context = {'request': request}
            # serializer = self.serializer_class(adresse, context=serializer_context)
            # return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise ValidationError(detail={"detail": "Vous n'avez pas d'adresse enregistrée !"})


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


class UserDemandeDevisRUApiView(generics.RetrieveUpdateAPIView):
    queryset = DemandeDevis.objects.all()
    serializer_class = UserDemandeDevisSerializer
    permission_classes = [IsAuthenticated]


class UserDevisListApiView(generics.ListAPIView):
    queryset = Devis.objects.all()
    serializer_class = AdminDevisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request_user = self.request.user
        devis = Devis.objects.filter(ref_demande_devis__ref_user_id=request_user, est_soumis=True)
        return devis


class UserDevisUpdateAPIView(generics.UpdateAPIView):
    queryset = Devis.objects.all()
    serializer_class = UserDevisAccepterSerializer
    permission_classes = [IsAuthenticated, ]


class ArticleLikeAPIView(views.APIView):
    serializer_class = ArticleSerializer
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


class RendezVousViewSet(generics.ListCreateAPIView):
    """
    TODO - url manquant
    TODO - Compléter le test sur une réservation de rendez-vous
    """
    queryset = RendezVous.objects.all()
    lookup_field = "pk"
    serializer_class = UserRendezVousSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = RendezVous.objects.filter(ref_user=self.request.user)
        serializer = UserRendezVousSerializer(queryset, many=True)
        return serializer.data

    def perform_create(self, serializer):
        request_user = self.request.user
        kwarg_date = datetime.strptime(str(serializer.validated_data["date"]), "%Y-%m-%d").date()
        now = datetime.now().date()
        kwarg_start = serializer.validated_data["start"]
        ref_type_service = serializer.validated_data["ref_type_service"]
        type_service = TypeService.objects.get(pk=ref_type_service.id)

        for debut in range(0, 240, 60):
            fin = debut + 60
            if debut < type_service.duree_minute <= fin:
                type_service.duree_minute = fin
                break
            elif type_service.duree_minute > 240:
                type_service.duree_minute = 240
                break
            else:
                fin += debut

        result = datetime.strptime(str(kwarg_start), "%H:%M:%S") + timedelta(minutes=type_service.duree_minute)
        kwarg_end = result.time()
        day = datetime.strptime(str(kwarg_date), "%Y-%m-%d").weekday()
        horaire = Horaire.objects.get(jour_semaine=day)
        if kwarg_date <= now:
            raise ValidationError(
                detail={'detail': "La date choisie ne peut pas être inférieur ou égale à celle d'aujourd'hui !"},
                code=status.HTTP_400_BAD_REQUEST
            )
        elif RendezVous.objects.filter(date=kwarg_date, start=kwarg_start, est_annule=False):
            raise ValidationError(
                detail={'detail': "Il y a déja une réservation pour cette heure, veillez choisir une heure disponible !"},
                code=status.HTTP_400_BAD_REQUEST
            )
        elif RendezVous.objects.filter(date=kwarg_date, est_annule=False).filter(Q(start__gt=kwarg_start) & Q(end__lte=kwarg_end)):
            raise ValidationError(
                detail={'detail': "Cette tranche pour ce service n'est pas possible !"},
                code=status.HTTP_400_BAD_REQUEST
            )
        elif kwarg_date == now:
            raise ValidationError(
                detail={'detail': "Le rendez-vous n'est pas possible pour le jour même !"},
                code=status.HTTP_400_BAD_REQUEST
            )
        elif horaire.sur_rdv is False and horaire.est_ferme is False:
            raise ValidationError(
                detail={'detail': "Nous sommes ouvert ce jour sans rendez-vous, veillez choisir un autre jour !"},
                code=status.HTTP_400_BAD_REQUEST
            )
        elif horaire.est_ferme:
            raise ValidationError(
                detail={'detail': "C'est fermé ce jour, choisisez un autre jour !"},
                code=status.HTTP_400_BAD_REQUEST
            )
        elif horaire.sur_rdv is True & (kwarg_start < horaire.heure_ouverture or kwarg_end > horaire.heure_fermeture):
            ouvert = horaire.heure_ouverture
            ferme = horaire.heure_fermeture
            pause_debut = horaire.pause_debut
            pause_fin = horaire.pause_fin
            raise ValidationError(
                detail={'detail': f'Veuillez choisir une heure de {ouvert} à {pause_debut} et de {pause_fin} à {ferme}'},
                code=status.HTTP_400_BAD_REQUEST
            )
        elif horaire.sur_rdv is True and (horaire.pause_debut < kwarg_end <= horaire.pause_fin):
            raise ValidationError(
                detail={
                    'detail': "Le rendez-vous pour ce service pour cette heure n'est pas possible, veuillez choisir une autre heure disponible !"
                },
                code=status.HTTP_400_BAD_REQUEST
            )
        else:
            serializer.save(ref_user=request_user, end=kwarg_end)


class AvailableHours(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        date_str = self.kwargs.get('date')
        queryset = RendezVous.objects.filter(date=date_str, est_annule=False)

        jour_semaine = datetime.strptime(date_str, '%Y-%m-%d').weekday()
        horaire = get_object_or_404(Horaire, jour_semaine=jour_semaine)

        available_hours = []

        if horaire.est_ferme is True:
            message = f'Nous sommes fermés le {date_str}'
            available_hours = []
        elif horaire.sur_rdv is False:
            ouverture = horaire.heure_ouverture
            fermeture = horaire.heure_fermeture
            pause_midi = horaire.pause_debut
            pause_fin = horaire.pause_fin
            message = f'Nous sommes ouvert sans rendez-vous le {date_str} de {ouverture} à {pause_midi} et de {pause_fin} à {fermeture}'
            available_hours = []

        else:
            start_time = datetime.strptime(str(horaire.heure_ouverture), '%H:%M:%S')
            end_time = datetime.strptime(str(horaire.heure_fermeture), '%H:%M:%S')
            pause_debut = datetime.strptime(str(horaire.pause_debut), '%H:%M:%S')
            pause_fin = datetime.strptime(str(horaire.pause_fin), '%H:%M:%S')

            message = f'Les heures disponible pour {date_str}'

            rdv_existant = []
            for q in queryset.iterator():
                rdv_existant.append(q.start)

            for n in range(start_time.hour, end_time.hour, 1):
                if pause_debut.hour <= n < pause_fin.hour:
                    pass
                else:
                    available_hours.append(start_time.time())
                delta = timedelta(hours=1)
                heure = datetime.strptime(str(start_time.time()), '%H:%M:%S')
                start_time = heure + delta

            for heure in rdv_existant:
                if heure in available_hours:
                    available_hours.remove(heure)

        context = {
            'message': message,
            'available_hours': available_hours
        }
        return Response(context)
