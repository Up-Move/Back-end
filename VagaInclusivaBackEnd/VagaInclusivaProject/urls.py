# pylint: disable=all

"""
Módulo que contém funções relacionadas as rotas do Projeto
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from geo.views import VagasAPIView

#Swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

#Viewsets
from Autenticacao.API.viewsets import UserViewSet, RegisterViewSet, RegisterValidationViewSet 
from avaliacao.views import GetAvaliacaoVagaView, PostAvaliacaoView, FiltroAPIView, FiltroUserAPIView, AvaliacaoListAPIView, RespostaAPIView
from MailService.views import send_email_view, change_password, atualizar_senha, atualizar_email, deletar_conta

SchemaView = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API Documentation",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Routers
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'auth/registration', RegisterViewSet)
router.register(r'register-validation', RegisterValidationViewSet)

urlpatterns = [
    #Administrador
    path('admin/', admin.site.urls),
    #Outras Outras
    path('', include(router.urls)),
    #Autenticação
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/login/', include('dj_rest_auth.urls')),
    #path('auth/registration/', include('dj_rest_auth.registration.urls')),
    #Documentação Swagger
    path('swagger/', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', SchemaView.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Victor
    path('vagas/', VagasAPIView.as_view()),
    path('avaliacoes/', PostAvaliacaoView.as_view(), name='criar_avaliacao'),
    path('avaliacoes/vaga/<int:id_vaga>/', GetAvaliacaoVagaView.as_view(), name='obter_avaliacao_vaga'),
    path('avaliacoes/lista/', AvaliacaoListAPIView.as_view(), name='avaliacoes-list'),
    path('filtro/', FiltroAPIView.as_view(), name='filtro-create'),
    path('filtro/user/<int:user_id>/', FiltroUserAPIView.as_view(), name='filtro-list'),
    path('avaliacoes/respostas/', RespostaAPIView.as_view(), name='resposta-list-create'),
    # Vinicius / Token e Senha
    path('email/', send_email_view, name='send_email'),
    path('newpassword/', change_password, name='change_password'),
    path('atualizar-senha/', atualizar_senha, name='atualizar_senha'),
    path('atualizar-email/', atualizar_email, name='atualizar_email'),
    path('deletar-conta/', deletar_conta, name='deletar_conta'),
]
