# pylint: disable=R0903, W0223

"""
Modulo que contem os serializers da API
"""

from rest_framework import serializers
from Autenticacao.models import User

# Mapear os Campos que irão aparecer no Django REST Framework
class UserSerializer(serializers.ModelSerializer):
    """
    Serializador do Usuário
    """
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True) ##
    class Meta:
        """
        Classe Meta
        """
        model = User
        fields = ['id', 'username', 'email', 'password']

# Serializador personalizado para o login
class CustomLoginSerializer(serializers.Serializer):
    """
    Serializador Custom de Login
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    key = serializers.CharField(read_only=True)
