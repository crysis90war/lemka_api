from django.urls import path

from lemka.views import *

app_name = 'public-api'

urlpatterns = [
    path('<int:pk>/articles/', ArticleServiceListAPIView.as_view(), name='articles-service'),

    path('catalogues/<rayon_slug>/', ArticleRayonListAPIView.as_view(), name='articles-rayon'),
    path('catalogues/<rayon_slug>/<section_slug>/', ArticleSectionListAPIView.as_view(), name='articles-section'),
    path('catalogues/<rayon_slug>/<section_slug>/<type_produit_slug>/', ArticleTypeProduitListAPIView.as_view(), name='articles-type-produit'),

    path('merceries/', GlobalMercerieListApiView.as_view(), name='global-merceries')
]