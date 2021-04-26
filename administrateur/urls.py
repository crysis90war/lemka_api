from django.urls import path, include
from rest_framework.routers import DefaultRouter

from administrateur.views import *

router = DefaultRouter()

router.register('pays', PaysViewSet)
router.register('villes', VilleViewSet)
router.register('genres', GenreViewSet)
router.register('types_services', TypeServiceViewSet)
router.register('rayons', RayonViewSet)
router.register('sections', SectionViewSet)
router.register('type_produits', TypeProduitViewSet)
router.register('tags', TagViewSet)
router.register('caracteristiques', CaracteristiqueViewSet)
router.register('couleurs', CouleurViewSet)
router.register('mensurations', MensurationViewSet)
router.register('categories', CategorieViewSet)
router.register('tva', TvaViewSet),
router.register('entreprises', EntrepriseLemkaViewSet)

router.register('catalogues', CatalogueViewSet)
router.register('demandes_devis', DemandeDevisViewSet)
router.register('devis', DevisViewSet)
router.register('details', DetailViewSet)
# router.register('rendezvous', RendezVousViewSet)
router.register('horaire', HoraireViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Récupération, création et détail avec update et supprésion d'images pour un article donné
    path('articles/', ArticleListCreateAPIView.as_view()),
    path('articles/<slug:slug>/', ArticleRUDApiView.as_view()),

    path('articles/<slug:slug>/images/', ArticleImageListCreateAPIView.as_view()),
    path('articles/<slug:slug>/images/<int:pk>/', ArticleImageRUDAPIView.as_view()),

    # Récupération, création et détail avec update et supprésion d'images pour un mercerie donné
    path('devis/<str:devis_id>/details/', DetailsListCreateApiView.as_view()),
    path('devis/<str:devis_id>/details/<int:pk>/', DetailRUDApiView.as_view()),

    # Récupération, création et détail avec update et suppréssion de mercerie
    path('merceries/', MercerieListCreateApiView.as_view()),
    path('merceries/<int:pk>/', MercerieRUDApiView.as_view()),

    path('merceries/<int:mercerie_id>/images/', MercerieImageCreateApiView.as_view()),
    path('merceries/<int:mercerie_id>/images/<int:pk>/', MercerieImageDestroyAPIView.as_view()),

    path('merceries/<int:mercerie_id>/characteristiques/', MercerieCaracteristiqueCreateApiView.as_view()),
    path('merceries/<int:mercerie_id>/characteristiques/<int:pk>/', MercerieCaracteristiqueRUDApiView.as_view()),

    # Récupération, détail et update d'utilisateurs
    path('utilisateurs/', UserListAPIView.as_view()),
    path('utilisateurs/<str:username>/', UserRetrieveAPIView.as_view()),

    path('utilisateurs/<str:username>/adresse/', UserAdresseRUDApiView.as_view()),
    path('utilisateurs/<str:username>/mensurations/', UserMensurationsListApiView.as_view()),

    path('check/<str:username>/', CheckUserAPIView.as_view()),
    path('admin-dashboard/', Dashboard.as_view())
]
