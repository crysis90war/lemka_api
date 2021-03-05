from django.urls import path

from lemka.views import *

urlpatterns = [
    path('public/horaire/', HoraireListAPIView.as_view(), name='horaire-public'),

    path('public/articles/<int:pk>/', ArticleServiceListAPIView.as_view(), name='article-service-list'),

    path('public/catalogues/<rayon_slug>/', ArticleRayonListAPIView.as_view(), name='article-rayon-list'),
    path('public/catalogues/<rayon_slug>/<section_slug>/', ArticleSectionListAPIView.as_view(), name='article-section-list'),
    path('public/catalogues/<rayon_slug>/<section_slug>/<type_produit_slug>/', ArticleTypeProduitListAPIView.as_view(), name='article-type-produit-list'),

    path('articles/<slug:slug>/like/', ArticleLikeAPIView.as_view(), name='article-like'),
]
