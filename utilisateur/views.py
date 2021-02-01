from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from lemka.permissions import UserGetPostPermission, UserRUDPermission
from lemka.serializers import *


class GenreListAPIView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated, ]


class GenreRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated, ]


class VillesListAPIView(generics.ListAPIView):
    queryset = Ville.objects.all()
    serializer_class = VilleSerializer
    permission_classes = [AllowAny, ]


class ProfilAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfilSerializer
    permission_classes = [IsAuthenticated, UserRUDPermission, ]

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
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        kwarg_id = self.kwargs.get('ref_user_mensuration_id')
        return MensurationUserMensuration.objects.filter(ref_user_mensuration=kwarg_id)


class MensurationUserMensurationUpdateApiView(generics.RetrieveUpdateAPIView):
    queryset = MensurationUserMensuration.objects.all()
    serializer_class = MensurationUserMensurationSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        kwarg_ref_user_mensuration_id = self.kwargs.get('ref_user_mensuration_id')
        return MensurationUserMensuration.objects.filter(
            ref_user_mensuration_id=kwarg_ref_user_mensuration_id,
        )


class AdresseListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = UserAdresseSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        if self.request.user and not self.request.user.is_anonymous:
            user = self.request.user
            queryset = Adresse.objects.filter()
            return queryset
        else:
            raise ValidationError("Les utilisateurs anonymes ne disposent d'aucun droit !")

    def perform_create(self, serializer):
        request_user = self.request.user
        adresses = Adresse.objects.filter(ref_user=request_user)

        if adresses.count() >= 2:
            raise ValidationError(
                "Vous avez deux adresses enregistrés, Veuillez modifier ou supprimer pour ajour un nouveau !")

        serializer.save(ref_user=request_user)


class AdresseRUDApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Adresse.objects.all()
    serializer_class = AdresseSerializer
    permission_classes = [UserRUDPermission, ]

    def get_queryset(self):
        if self.request.user and not self.request.user.is_anonymous:
            queryset = Adresse.objects.filter(ref_user=self.request.user)
            return queryset
        else:
            return ValidationError('Vous devez vous connecter')
            # raise exceptions.AuthenticationFailed('Vous devez vous connecter')
