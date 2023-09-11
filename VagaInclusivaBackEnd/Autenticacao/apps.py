"""
Modulo que contem os Apps do Projeto
"""

from django.apps import AppConfig

class AutenticacaoConfig(AppConfig):
    """
    Configurações do App Autenticação
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Autenticacao'
