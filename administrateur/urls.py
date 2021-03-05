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
router.register('catalogues', CatalogueViewSet)
router.register('tags', TagViewSet)
# router.register('articles', ArticleViewSet)
router.register('entreprise', EntrepriseLemkaViewSet)
router.register('accomptedemande', AccompteDemandeViewSet)
router.register('couleurs', CouleurViewSet)
router.register('categories', CategorieViewSet)
# router.register('merceries', MercerieViewSet)
# router.register('mercerieoption', MercerieCouleurViewSet)
router.register('details', DetailViewSet)
router.register('tva', TvaViewSet),
router.register('mensurations', MensurationViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('articles/', ArticleListAPIView.as_view(), name='article-list'),
    path('articles/new/', ArticleCreateAPIView.as_view(), name='article-create'),
    path('articles/<slug:slug>/', ArticleRUDApiView.as_view(), name='article-rud'),

    # Récupération, création et détail avec update et supprésion d'images pour un article donné
    path('articles/<slug:slug>/images/', ArticleImageListCreateAPIView.as_view(), name='article-image-list-create'),
    path('articles/<slug:slug>/images/<int:pk>/', ArticleImageRUDAPIView.as_view(), name='article-image-detail'),

    # Récupération, création et détail avec update et supprésion d'images pour un mercerie donné
    # path('merceries/<int:pk>/images/', MercerieCouleurImageListCreateAPIView.as_view(), name='mercerie-couleur-image-list-create'),
    # path('merceries/<int:pk>/images/<int:id>/', MercerieCouleurImageRUDAPIView.as_view(), name='mercerie-couleur-image-detail'),

    # Récupération, création et détail avec update et supprésion d'images pour un mercerie donné
    path('devis/<str:numero_devis>/details/', DetailListAPIView.as_view(), name='detail-list'),
    path('devis/<str:numero_devis>/details/', DetailCreateAPIView.as_view(), name='detail-create'),
    path('devis/<str:numero_devis>/<int:pk>/', DetailRUDApiView.as_view(), name='detail-detail'),

    # Récupération, création et détail avec update et suppréssion de mercerie
    path('merceries/', MercerieListCreateApiView.as_view()),
    path('merceries/<int:pk>/', MercerieRUDApiView.as_view()),

    path('merceries/<int:mercerie_id>/options/', MercerieOptionListCreateApiView.as_view()),
    path('merceries/<int:mercerie_id>/options/<int:pk>/', MercerieOptionRUDApiView.as_view()),

    path('mercerie_options/<int:mercerie_option_id>/images/', MercerieOptionImageListCreateApiView.as_view()),
    path('mercerie_options/<int:mercerie_option_id>/images/<int:pk>/', MercerieOptionImageRUDApiView.as_view()),

    # Récupération, détail et update d'utilisateurs
    path('utilisateurs/', UserListAPIView.as_view(), name='customuser-list'),
    path('utilisateurs/<str:username>/', UserRetrieveAPIView.as_view(), name='customuser-detail'),

    path('utilisateurs/<str:username>/adresses/', UserAdresseRUDApiView.as_view()),

    path('check/<str:username>/', CheckUserAPIView.as_view(), name='very-user-exists'),
    path('admin-dashboard/', Dashboard.as_view(), name='admin-dashboard')
]
