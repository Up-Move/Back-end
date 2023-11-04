from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

# Construtor para as excessões
class CustomAuthException(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(message)

# Responsavel pela Autenticação com E-Mail
class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            # Para Caso o Email não tenha sido cadastrado no banco de dados
            raise CustomAuthException(500, 'Email não encontrado no banco de dados')
        else:
            if user.check_password(password):
                return user
            else:
            # Para Não ter Nenhum outro Erro 500
                return None