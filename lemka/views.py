from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Count
from django.db.models import Q
from django.http import HttpResponsePermanentRedirect
from django.template.loader import get_template
from django.urls import reverse
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode
from django_filters import rest_framework as df_filters
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from lemka.filters import GlobalArticleFilter, GlobalMercerieFilter
from lemka.pagination import SmallSetPagination
from lemka.permissions import UserGetPostPermission, IsOwner, IsAdminOrReadOnly
from lemka.serializers import *
from lemka_api.utils import Utils
from rest_framework import viewsets, generics, filters, status


# region Auth

class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GoogleSocialAuthView(GenericAPIView):
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST avec "auth_token"
        Envoyez un identifiant à partir de Google pour obtenir des informations utilisateur
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


class FacebookSocialAuthView(GenericAPIView):
    serializer_class = FacebookSocialAuthSerializer

    def post(self, request):
        """
        POST avec "auth_token"
        Envoyez un jeton d'accès à partir de Facebook pour obtenir des informations utilisateur
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    # TODO - rediriger user vers front-end avec url et token d'activation.

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse('users-auth-api:email-verify')

        absurl = 'https://' + current_site + relative_link + '?token=' + str(token)
        email_body_html = get_template('lemka/register_template.html').render(dict({
            'username': user.username,
            'url': absurl
        }))
        email_body = f'Bonjour {user.username}, cliquez sur le lien suivant pour activer votre compte ... {absurl}'
        data = {
            # 'email_body': email_body,
            'email_body': email_body_html,
            'to_email': user.email,
            'email_subject': "Vérification d'email"
        }
        Utils.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmailView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter(
        'token',
        in_=openapi.IN_QUERY,
        description='Description',
        type=openapi.TYPE_STRING
    )

    # noinspection PyMethodMayBeStatic
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        redirect_url = request.GET.get('redirect_url', 'http://localhost:8080/email-verify/')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return CustomRedirect(
                redirect_url + '?token_valid=True&message=Votre compte a été activé avec succès&token=' + token)
            # return Response({'email': 'Activé avec succès'}, status=status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError as identifier:
            return CustomRedirect(redirect_url + '?token_valid=False&message=Activtaion expiré&token=' + token)
            # return Response({'error': 'Activtaion expiré'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return CustomRedirect(redirect_url + '?token_valid=False&message=Jeton invalide&token=' + token)
            # return Response({'error': 'Jeton invalide'}, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email, auth_provider='email').exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request).domain
            relative_link = reverse('users-auth-api:password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'https://' + current_site + relative_link
            email_body_html = get_template('lemka/reset_password_template.html').render(dict({
                'username': user.username,
                'absurl': absurl,
                'redirect_url': redirect_url
            }))
            email_body = 'Hello, \n Use link below to reset your password  \n' + absurl + "?redirect_url=" + redirect_url
            data = {
                # 'email_body': email_body,
                'email_body': email_body_html,
                'to_email': user.email,
                'email_subject': 'Reset your passsword'
            }
            Utils.send_email(data)
        return Response(
            {
                'success': 'Nous vous avons envoyé un lien pour réinitialiser votre mot de passe'
            },
            status=status.HTTP_200_OK
        )


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url + '?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(
                    redirect_url + '?token_valid=True&message=Identifiants Valides&uidb64=' + uidb64 + '&token=' + token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url + '?token_valid=False')

            except UnboundLocalError as e:
                return Response({'error': "Le jeton n'est pas valide, veuillez en demander un nouveau"},
                                status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# endregion


# region Utilisateur

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


class UserMesureListApiView(generics.ListAPIView):
    queryset = UserMesure.objects.all()
    serializer_class = UserMesureSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        kwarg_user = self.request.user
        kwarg_id = self.kwargs.get('ref_user_mensuration_id')
        return UserMesure.objects.filter(ref_user_mensuration=kwarg_id, ref_user_mensuration__ref_user=kwarg_user)


class UserMesureRUApiView(generics.RetrieveUpdateAPIView):
    queryset = UserMesure.objects.all()
    serializer_class = UserMesureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        ref_mensuration = self.kwargs.get('pk')
        if UserMesure.objects.filter(id=ref_mensuration).exists():
            obj2 = UserMesure.objects.get(id=ref_mensuration)
            owner = obj2.ref_user_mensuration.ref_user
            if owner == user:
                return UserMesure.objects.filter(id=ref_mensuration)

    def perform_update(self, serializer):
        user = self.request.user
        ref_mensuration = self.kwargs.get('pk')
        if UserMesure.objects.filter(id=ref_mensuration).exists():
            obj2 = UserMesure.objects.get(id=ref_mensuration)
            owner = obj2.ref_user_mensuration.ref_user
            if owner == user:
                serializer.save()


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


# class ArticleLikeAPIView(views.APIView):
#     serializer_class = ArticleSerializer
#     permission_classes = [IsAuthenticated]
#
#     def delete(self, request, slug):
#         article = get_object_or_404(Article, slug=slug)
#         user = request.user
#         article.likes.remove(user)
#         article.save()
#
#         serializer_context = {'request': request}
#         serializer = self.serializer_class(article, context=serializer_context)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request, slug):
#         article = get_object_or_404(Article, slug=slug)
#         user = request.user
#         article.likes.add(user)
#         article.save()
#
#         serializer_context = {'request': request}
#         serializer = self.serializer_class(article, context=serializer_context)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class RendezVousListCreateAPIView(generics.ListCreateAPIView):
    queryset = RendezVous.objects.all()
    lookup_field = "pk"
    serializer_class = UserRendezVousSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = RendezVous.objects.filter(ref_user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        request_user = self.request.user
        kwarg_date = datetime.strptime(str(serializer.validated_data["date"]), "%Y-%m-%d").date()
        now = datetime.now().date()
        kwarg_start = serializer.validated_data["start"]
        ref_service = serializer.validated_data["ref_service"]
        service = Service.objects.get(pk=ref_service.id)

        for debut in range(0, 240, 60):
            fin = debut + 60
            if debut < service.duree_minute <= fin:
                service.duree_minute = fin
                break
            elif service.duree_minute > 240:
                service.duree_minute = 240
                break
            else:
                fin += debut

        result = datetime.strptime(str(kwarg_start), "%H:%M:%S") + timedelta(minutes=service.duree_minute)
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
                detail={
                    'detail': "Il y a déja une réservation pour cette heure, veillez choisir une heure disponible !"},
                code=status.HTTP_400_BAD_REQUEST
            )
        elif RendezVous.objects.filter(date=kwarg_date, est_annule=False).filter(
                Q(start__gt=kwarg_start) & Q(end__lte=kwarg_end)):
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
                detail={
                    'detail': f'Veuillez choisir une heure de {ouvert} à {pause_debut} et de {pause_fin} à {ferme}'},
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


class RendezVousUpdateAPIView(generics.UpdateAPIView):
    queryset = RendezVous.objects.all()
    serializer_class = AnnulerRendezVousSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        kward_user = self.request.user
        obj = self.get_object()
        if obj.ref_user == kward_user:
            if obj.est_annule is True:
                raise ValidationError(
                    detail={'detail': "Le rendez-vous est annulé. Veuillez demander un nouveau !"},
                    code=status.HTTP_400_BAD_REQUEST
                )
            elif obj.date < datetime.now().date():
                raise ValidationError(
                    detail={'detail': "Vous ne pouvez pas annuler les rendez-vous antérieur à la date d'aujourd'hui !"},
                    code=status.HTTP_400_BAD_REQUEST
                )
            else:
                serializer.save()
        else:
            raise ValidationError(
                detail={'detail': "Vous n'avez pas le droit d'accès aux données autres que les vôtres !"},
                code=status.HTTP_400_BAD_REQUEST
            )


class AvailableHoursAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        date_str = self.kwargs.get('date')
        queryset = RendezVous.objects.filter(date=date_str, est_annule=False)

        jour_semaine = datetime.strptime(date_str, '%Y-%m-%d').weekday()
        horaire = get_object_or_404(Horaire, jour_semaine=jour_semaine)

        available_hours = []
        heures_dispos = []

        if horaire.est_ferme is True:
            message = f'Nous sommes fermés le {date_str}'
        elif horaire.sur_rdv is False:
            ouverture = horaire.heure_ouverture
            fermeture = horaire.heure_fermeture
            pause_midi = horaire.pause_debut
            pause_fin = horaire.pause_fin
            message = f'Nous sommes ouvert sans rendez-vous le {date_str} de {ouverture} à {pause_midi} et de {pause_fin} à {fermeture}'

        else:
            start_time = datetime.strptime(str(horaire.heure_ouverture), '%H:%M:%S')
            end_time = datetime.strptime(str(horaire.heure_fermeture), '%H:%M:%S')
            pause_debut = datetime.strptime(str(horaire.pause_debut), '%H:%M:%S')
            pause_fin = datetime.strptime(str(horaire.pause_fin), '%H:%M:%S')

            message = f'Les heures disponible pour {date_str}'

            rdv_existant = []
            '''
            Les rendez-vous existant
            '''
            for q in queryset.iterator():
                existing = {
                    'start': q.start,
                    'end': q.end
                }
                rdv_existant.append(existing)

            """
            Les heures disponibles par rapport a l'horaire
            """
            for n in range(start_time.hour, end_time.hour, 1):
                if pause_debut.hour <= n < pause_fin.hour:
                    pass
                else:
                    horaire = {
                        'start': start_time.time(),
                        'end': (datetime.strptime(str(start_time.time()), '%H:%M:%S') + timedelta(hours=1)).time()
                    }
                    available_hours.append(horaire)
                delta = timedelta(hours=1)
                heure = datetime.strptime(str(start_time.time()), '%H:%M:%S')
                start_time = heure + delta

            '''
            Retirer les heures de rendez-vous existant dans les heures disponibles de l'horaire.
            '''
            for heure in rdv_existant:
                if heure in available_hours:
                    available_hours.remove(heure)
                for dispo in available_hours:
                    if dispo['start'].hour < heure['end'].hour <= dispo['end'].hour:
                        heure_existant = {
                            'start': heure['start'],
                            'end': (datetime.strptime(str(heure['start']), '%H:%M:%S') + timedelta(hours=1)).time()
                        }
                        available_hours.remove(dispo)
                        available_hours.remove(heure_existant)

            for heure in available_hours:
                hour = datetime.strptime(str(heure['start']), '%H:%M:%S')
                heures_dispos.append(hour.time())

        context = {
            'message': message,
            'available_hours': heures_dispos
        }
        return Response(context, status=status.HTTP_200_OK)


# endregion


# region public

class ArticleServiceListAPIView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        kwarg_service = self.kwargs.get("pk")
        return Article.objects.filter(ref_service__id=kwarg_service, est_active=True)


class ArticleRayonListAPIView(ArticleServiceListAPIView):

    def get_queryset(self):
        kwarg_rayon_slug = self.kwargs.get("rayon_slug")
        return Article.objects.filter()


class ArticleSectionListAPIView(ArticleServiceListAPIView):

    def get_queryset(self):
        kwarg_rayon_slug = self.kwargs.get("rayon_slug")
        kwarg_section_slug = self.kwargs.get("section_slug")
        return Article.objects.filter()


class ArticleTypeProduitListAPIView(ArticleServiceListAPIView):

    def get_queryset(self):
        kwarg_rayon_slug = self.kwargs.get("rayon_slug")
        kwarg_section_slug = self.kwargs.get("section_slug")
        kwarg_type_produit_slug = self.kwargs.get("type_produit_slug")
        return Article.objects.filter()


class GlobalMercerieListApiView(generics.ListAPIView):
    queryset = Mercerie.objects.all().filter(est_publie=True)
    serializer_class = GlobalMercerieSerializer
    filter_backends = [df_filters.DjangoFilterBackend]
    filterset_class = GlobalMercerieFilter


class GlobalArticlesListApiView(generics.ListAPIView):
    queryset = Article.objects.filter(est_active=True)
    serializer_class = GlobalArticleSerializer
    filter_backends = [df_filters.DjangoFilterBackend]
    filterset_class = GlobalArticleFilter


class LastArticleListAPIView(generics.ListAPIView):
    queryset = Article.objects.filter(est_active=True).order_by('-created_at')[:10]
    serializer_class = GlobalArticleSerializer


class GlobalPopularArticleListAPIView(generics.ListAPIView):
    queryset = Article.objects.filter(est_active=True).annotate(likes_count=Count('likes')).order_by('-likes_count')[
               :10]
    serializer_class = GlobalArticleSerializer


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


# endregion


# region Administration

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


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().order_by("nom")
    serializer_class = ServiceSerializer
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

# endregion
