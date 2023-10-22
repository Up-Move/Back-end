"""
Modulo que contem os Models do Projeto
"""

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Modulo de Usuário Custom
    """
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)


class UserKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=64, unique=True)
