from django.urls import path, include
from rest_framework.routers import DefaultRouter

from utilisateur.views import *

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('profil/', ProfilAPIView.as_view()),

    path('profil/adresse/create', AdresseCreateAPIView.as_view()),  # CREATE adresse
    path('profil/adresse/', AdresseRUDAPIView.as_view()),  # GET PUT PATCH DELETE adresse

    path('profil/mensurations/', UserMensurationListCreateAPIView.as_view()),
    path('profil/mensurations/<int:pk>/', UserMensurationRUDApiView.as_view()),
    path('profil/mensurations/<int:ref_user_mensuration_id>/mesures/', MensurationUserMensurationListApiView.as_view()),
    path('profil/mensurations/<int:ref_user_mensuration_id>/mesures/<int:pk>/', MensurationUserMensurationUpdateApiView.as_view()),

    path('demandes_devis/', UserDemandeDevisListCreateApiView.as_view()),

    path('articles/<slug:slug>/like/', ArticleLikeAPIView.as_view(), name='article-like'),

    # TODO - Devis
    # TODO - Bon de commande
    # TODO - Facture
    # TODO - Rendez-vous
]
