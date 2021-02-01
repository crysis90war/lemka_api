from django.urls import path, include
from rest_framework.routers import DefaultRouter

from administrateur.views import HoraireViewSet
from lemka.views import DemandeDevisViewSet, DevisViewSet, RendezVousViewSet
from utilisateur.views import *

router = DefaultRouter()

router.register('demandedevis', DemandeDevisViewSet)
router.register('devis', DevisViewSet)
router.register('rendezvous', RendezVousViewSet)
router.register('horaire', HoraireViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('profil/', ProfilAPIView.as_view()),
    path('profil/genres/', GenreListAPIView.as_view()),
    path('profil/genres/<int:pk>/', GenreRetrieveAPIView.as_view()),

    path('user_mensurations/', UserMensurationListCreateAPIView.as_view()),
    path('user_mensurations/<int:pk>/', UserMensurationRUDApiView.as_view()),
    path('user_mensurations/<int:ref_user_mensuration_id>/mensurations/', MensurationUserMensurationListApiView.as_view()),
    path('user_mensurations/<int:ref_user_mensuration_id>/mensurations/<int:pk>/', MensurationUserMensurationUpdateApiView.as_view()),

    path('user_adresses/villes/', VillesListAPIView.as_view()),
    path('user_adresses/', AdresseListCreateAPIView.as_view()),
    path('user_adresses/<int:pk>/', AdresseRUDApiView.as_view())
]