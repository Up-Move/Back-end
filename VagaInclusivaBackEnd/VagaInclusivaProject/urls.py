"""
Módulo que contém funções relacionadas as rotas do Projeto
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

#Swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

#Viewsets
from Autenticacao.API.viewsets import UserViewSet
from Autenticacao.API.viewsets import RegisterViewSet

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
]
