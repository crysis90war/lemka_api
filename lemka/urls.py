from django.urls import path

from lemka.views import *

app_name = 'public-api'

urlpatterns = [
    path('<int:pk>/articles/', ArticleServiceListAPIView.as_view(), name='articles-service'),

    path('merceries/', GlobalMercerieListApiView.as_view(), name='global-merceries'),
    path('articles/', GlobalArticlesListApiView.as_view(), name='global-articles'),
    path('popular/', GlobalPopularArticleListAPIView.as_view(), name='popular-articles'),
    path('last/', LastArticleListAPIView.as_view(), name='last-articles'),
]