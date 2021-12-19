from django.urls import path, include
from rest_framework.routers import DefaultRouter

from lemka.views import *

app_name = 'public-api'


router = DefaultRouter()

router.register('pays', PaysViewSet)
router.register('villes', VilleViewSet)
router.register('genres', GenreViewSet)
router.register('services', ServiceViewSet)
router.register('rayons', RayonViewSet)
router.register('sections', SectionViewSet)
router.register('type-produits', TypeProduitViewSet)
router.register('tags', TagViewSet)
router.register('caracteristiques', CaracteristiqueViewSet)
router.register('couleurs', CouleurViewSet)
router.register('mensurations', MensurationViewSet)
router.register('categories', CategorieViewSet)
router.register('tva', TvaViewSet),
router.register('entreprises', EntrepriseLemkaViewSet)
router.register('demandes_devis', DemandeDevisViewSet)
router.register('devis', DevisViewSet)
router.register('details', DetailViewSet)
router.register('rendezvous', RendezVousViewSet)
router.register('horaires', HoraireViewSet)

urlpatterns = [
    path('auth/test/', LoginAPIView.as_view()),
    path('auth/login/', MyTokenObtainPairView.as_view(), name='login'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/email-verify/', VerifyEmailView.as_view(), name='email-verify'),
    path('auth/request-reset-email/', RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('auth/password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('auth/password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
    path('auth/google/', GoogleSocialAuthView.as_view()),
    path('auth/facebook/', FacebookSocialAuthView.as_view()),

    path('public/<int:pk>/articles/', ArticleServiceListAPIView.as_view(), name='articles-service'),
    path('public/merceries/', GlobalMercerieListApiView.as_view(), name='global-merceries'),
    path('public/articles/', GlobalArticlesListApiView.as_view(), name='global-articles'),
    path('public/popular/', GlobalPopularArticleListAPIView.as_view(), name='popular-articles'),
    path('public/last/', LastArticleListAPIView.as_view(), name='last-articles'),

    path('profil/', ProfilAPIView.as_view()),
    path('profil/articles/<slug:slug>/like/', ArticleLikeAPIView.as_view(), name='article-like'),

    path('profil/adresse/create/', AdresseCreateAPIView.as_view()),  # CREATE adresse
    path('profil/adresse/', AdresseRUDAPIView.as_view()),  # GET PUT PATCH DELETE adresse

    path('profil/mensurations/', UserMensurationListCreateAPIView.as_view()),
    path('profil/mensurations/<int:pk>/', UserMensurationRUDApiView.as_view()),
    path('profil/mensurations/<int:ref_user_mensuration_id>/mesures/', UserMesureListApiView.as_view()),
    path('profil/mensurations/<int:ref_user_mensuration_id>/mesures/<int:pk>/', UserMesureRUApiView.as_view()),

    path('profil/demandes_devis/', UserDemandeDevisListCreateApiView.as_view()),
    path('profil/demandes_devis/<int:pk>/', UserDemandeDevisRUApiView.as_view()),

    path('profil/devis/', UserDevisListApiView.as_view()),
    path('profil/devis/<int:pk>/', UserDevisUpdateAPIView.as_view()),
    # path('profil/devis/<str:devis_numero>/details/<int:pk>/'),

    path('profil/rendez-vous/', RendezVousListCreateAPIView.as_view()),
    path('profil/rendez-vous/<int:pk>/', RendezVousUpdateAPIView.as_view()),
    # TODO - UPDATE RENDEZ-VOUS pour annuler (est_annule = False)

    path('profil/available-hours/<str:date>/', AvailableHoursAPIView.as_view()),
    path('profil/articles/<slug:slug>/like/', ArticleLikeAPIView.as_view(), name='article-like'),

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

    # TODO - Rendez-vous

    path('check/<str:username>/', CheckUserAPIView.as_view()),
    path('is-admin/', IsAdmin.as_view())
]