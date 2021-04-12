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

    path('articles/', ArticleListCreateAPIView.as_view(), name='article-list'),
    path('articles/<slug:slug>/', ArticleRUDApiView.as_view(), name='article-rud'),

    # Récupération, création et détail avec update et supprésion d'images pour un article donné
    path('articles/<slug:slug>/images/', ArticleImageListCreateAPIView.as_view(), name='article-image-list-create'),
    path('articles/<slug:slug>/images/<int:pk>/', ArticleImageRUDAPIView.as_view(), name='article-image-detail'),

    # Récupération, création et détail avec update et supprésion d'images pour un mercerie donné
    path('devis/<str:numero_devis>/details/', DetailsListCreateApiView.as_view()),
    path('devis/<str:numero_devis>/details/<int:pk>/', DetailRUDApiView.as_view()),

    # Récupération, création et détail avec update et suppréssion de mercerie
    path('merceries/', MercerieListCreateApiView.as_view()),
    path('merceries/<int:pk>/', MercerieRUDApiView.as_view()),

    path('merceries/<int:mercerie_id>/options/', MercerieOptionListCreateApiView.as_view()),
    path('merceries/<int:mercerie_id>/options/<int:pk>/', MercerieOptionRUDApiView.as_view()),

    path('mercerie_options/<int:mercerie_option_id>/images/', MercerieOptionImageListCreateApiView.as_view()),
    path('mercerie_options/<int:mercerie_option_id>/images/<int:pk>/', MercerieOptionImageRUDApiView.as_view()),

    path('mercerie_options/<int:mercerie_option_id>/caracteristiques/', MercerieOptionCaracteristiqueListCreateApiView.as_view()),
    path('mercerie_options/<int:mercerie_option_id>/caracteristiques/<int:pk>/', MercerieOptionCaracteristiqueRUDApiView.as_view()),

    # Récupération, détail et update d'utilisateurs
    path('utilisateurs/', UserListAPIView.as_view(), name='customuser-list'),
    path('utilisateurs/<str:username>/', UserRetrieveAPIView.as_view(), name='customuser-detail'),

    path('utilisateurs/<str:username>/adresses/', UserAdresseRUDApiView.as_view()),

    path('check/<str:username>/', CheckUserAPIView.as_view(), name='very-user-exists'),
    path('admin-dashboard/', Dashboard.as_view(), name='admin-dashboard')
]
