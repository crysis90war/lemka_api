from django.urls import path, include
from rest_framework.routers import DefaultRouter

from administrateur.views import HoraireViewSet
from lemka.views import DemandeDevisViewSet, DevisViewSet, RendezVousViewSet
from utilisateur.views import *

router = DefaultRouter()

# router.register('demandedevis', DemandeDevisViewSet)
router.register('devis', DevisViewSet)
router.register('rendezvous', RendezVousViewSet)
router.register('horaire', HoraireViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('profil/', ProfilAPIView.as_view()),

    path('profil/adresses/', AdresseCreateAPIView.as_view()),  # CREATE adresse
    path('profil/adresse/', AdresseAPIView.as_view()),  # GET PUT PATCH DELETE adresse

    path('profil/mensurations/', UserMensurationListCreateAPIView.as_view()),
    path('profil/mensurations/<int:pk>/', UserMensurationRUDApiView.as_view()),
    path('profil/mensurations/<int:ref_user_mensuration_id>/mensurations/',
         MensurationUserMensurationListApiView.as_view()),
    path('profil/mensurations/<int:ref_user_mensuration_id>/mensurations/<int:pk>/',
         MensurationUserMensurationUpdateApiView.as_view()),

    path('demandes_devis/', UserDemandeDevisListCreateApiView.as_view())
]
