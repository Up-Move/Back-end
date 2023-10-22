# pylint: disable=R0901

"""
Modulo que contem as Viewsets da API
"""

from rest_framework import viewsets
from Autenticacao.models import User
from Autenticacao.API.serializers import CustomLoginSerializer
from dj_rest_auth.views import LoginView
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from Autenticacao.models import UserKey
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Viewset Usuario
class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset do Usuário
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna apenas o perfil do usuário autenticado
        return User.objects.filter(id=self.request.user.id)

# Viewset Login
class CustomLoginView(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)

        if user:
            key, created = UserKey.objects.get_or_create(user=user)
            serialized_key = UserSerializer(key).data
            serialized_key['username'] = user.username
            return Response(serialized_key, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
