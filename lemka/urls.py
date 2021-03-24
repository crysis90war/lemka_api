from django.urls import path

from lemka.views import *

urlpatterns = [
    path('public/<int:pk>/articles/', ArticleServiceListAPIView.as_view()),

    path('public/catalogues/<rayon_slug>/', ArticleRayonListAPIView.as_view()),
    path('public/catalogues/<rayon_slug>/<section_slug>/', ArticleSectionListAPIView.as_view()),
    path('public/catalogues/<rayon_slug>/<section_slug>/<type_produit_slug>/', ArticleTypeProduitListAPIView.as_view()),

    path('public/merceries/', GlobalMercerieListApiView.as_view())
]