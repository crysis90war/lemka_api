from django.urls import include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse, reverse_lazy


@api_view(['GET'])
def api_root(request):
    """
    Single entry point to Lemka Api (Does not include dynamic urls)
    """

    return Response({
        'login': reverse('users-auth-api:login', request=request),
        'register': reverse('users-auth-api:register', request=request),
        # 'administration': include('administrateur.urls'),
    })
