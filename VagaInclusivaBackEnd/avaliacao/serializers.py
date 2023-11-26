from rest_framework import serializers
from django.contrib.gis.geos import GEOSGeometry


from Autenticacao.backends import User
from .models import Avaliacao, FiltroAcessibilidade, Filtro, Resposta, Acessibilidade
from geo.models import Vagas


class AvaliacaoSerializer(serializers.ModelSerializer):
    # Create a custom serializer field for the username
    user_username = serializers.CharField(source='user.username', read_only=True)
    username = serializers.CharField(write_only=True)

    class Meta:
        model = Avaliacao
        fields = '__all__'

    def create(self, validated_data):
        # Extract the username from the validated data
        username = validated_data.pop('username')

        # Find the user object based on the provided username
        user = User.objects.get(email=username)

        # Set the user ID on the Avaliacao object
        validated_data['user'] = user

        # Create and return the Avaliacao object
        avaliacao = Avaliacao.objects.create(**validated_data)
        return avaliacao


class AvaliacaoVagaSerializer(serializers.ModelSerializer):
    vaga_details = serializers.SerializerMethodField()

    class Meta:
        model = Vagas
        fields = ('index', 'total_avaliacoes', 'media_notas', 'vaga_details')

    def get_vaga_details(self, obj):
        # Converta o campo geometry para WKT
        local_geometry = GEOSGeometry(obj.geometry)
        local_wkt = local_geometry.wkt

        vaga_details = {
            'local': obj.local,
            'complemento': obj.complemento,
            'quantidadev': obj.quantidadev,
            'area': obj.area,
            'coordenadas': local_wkt  # Adicione o valor WKT ao dicionário
        }

        #print("Detalhes da Vaga:", vaga_details)

        return vaga_details

class AcessibilidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acessibilidade
        fields = ('id', 'tipo')


class FiltroAcessibilidadeSerializer(serializers.ModelSerializer):
    acessibilidade = AcessibilidadeSerializer()

    class Meta:
        model = FiltroAcessibilidade
        fields = ('acessibilidade',)


class FiltroSerializer(serializers.ModelSerializer):
    acess = serializers.SerializerMethodField()

    class Meta:
        model = Filtro
        fields = ('id', 'nome', 'acess', 'nota')

    def get_acess(self, obj):
        filtro_acessibilidades = FiltroAcessibilidade.objects.filter(filtro=obj)
        return [fa.acessibilidade.id for fa in filtro_acessibilidades]


class RespostaSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Resposta
        fields = ('id', 'user', 'avaliacao', 'comentario')
