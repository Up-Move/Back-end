# pylint: disable=R0901

"""
Modulo que contem as Viewsets da API
"""
from rest_framework import viewsets
from Autenticacao.models import User
from .serializers import UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError

# Responsavel pela Autenticação de Cadastro
class CustomAuthException(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(message)

# Viewset de Usuario
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

# Viewset Responsavel pelo Cadastro  
class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('username', None)
        password = request.data.get('password1', None)
        email = request.data.get('email', None)  # Adicione o campo de e-mail

        # Verifique se o usuário já existe no banco de dados
        try:
            user = User.objects.get(username=username)
            raise CustomAuthException(500, 'Usuário ja cadastrado no Banco')
        except User.DoesNotExist:
            user = None

        try:
            if user is None:
                user = User(username=username, email=email)
                user.save()
                user.set_password(password)
                user.save() 
                return Response({'message': 'Usuário registrado com sucesso'}, status=status.HTTP_201_CREATED)
        
        except IntegrityError as e: 
            return Response({'message': 'Erro de integridade: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'Usuário já existe'}, status=status.HTTP_400_BAD_REQUEST)
    

# Viewset Responsavel pelas Validações do Cadastro
class RegisterValidationViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('username', None)
        email = request.data.get('email', None)

        # Verifique se o usuário já existe no banco de dados
        try:
            user = User.objects.get(username=username)
            raise CustomAuthException(500, 'Usuário ja cadastrado no Banco')
        except User.DoesNotExist:
            user = None

        try:
            if user is None:
                user = User(username=username, email=email)
                user.save()
                user.delete()
                return Response({'message': 'Usuário verificado com sucesso'}, status=status.HTTP_201_CREATED)
        
        except IntegrityError as e: 
            return Response({'message': 'Erro de integridade: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'Usuário já existe'}, status=status.HTTP_400_BAD_REQUEST)

