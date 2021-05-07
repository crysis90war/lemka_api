from django.urls import path

from lemka.views import ArticleLikeAPIView
from utilisateur.views import *

urlpatterns = [
    path('', ProfilAPIView.as_view()),
    path('articles/<slug:slug>/like/', ArticleLikeAPIView.as_view(), name='article-like'),

    path('adresse/create/', AdresseCreateAPIView.as_view()),  # CREATE adresse
    path('adresse/', AdresseRUDAPIView.as_view()),  # GET PUT PATCH DELETE adresse

    path('mensurations/', UserMensurationListCreateAPIView.as_view()),
    path('mensurations/<int:pk>/', UserMensurationRUDApiView.as_view()),
    path('mensurations/<int:ref_user_mensuration_id>/mesures/', UserMensurationMesureListApiView.as_view()),
    path('mensurations/<int:ref_user_mensuration_id>/mesures/<int:pk>/', UserMensurationMesureRUApiView.as_view()),

    path('demandes_devis/', UserDemandeDevisListCreateApiView.as_view()),
    path('demandes_devis/<int:pk>/', UserDemandeDevisRUApiView.as_view()),

    path('devis/', UserDevisListApiView.as_view()),
    path('devis/<int:pk>/', UserDevisUpdateAPIView.as_view()),
    # path('profil/devis/<str:devis_numero>/details/<int:pk>/'),

    path('rendez-vous/', RendezVousListCreateAPIView.as_view()),
    path('rendez-vous/<int:pk>/', RendezVousUpdateAPIView.as_view()),
    # TODO - UPDATE RENDEZ-VOUS pour annuler (est_annule = False)

    path('available-hours/<str:date>/', AvailableHoursAPIView.as_view()),
    path('articles/<slug:slug>/like/', ArticleLikeAPIView.as_view(), name='article-like'),
]
