from rest_framework import serializers
from .models import Avaliacao, AvaliacaoVaga, FiltroAcessibilidade, Filtro, Resposta, Acessibilidade
from geo.models import Vagas


class AvaliacaoSerializer(serializers.ModelSerializer):
   # user = serializers.StringRelatedField()  # Example, you can customize this to include user details
   # vaga = serializers.StringRelatedField()  # Example, you can customize this to include vaga details

    class Meta:
        model = Avaliacao
        fields = '__all__'


class NestedVagasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vagas
        fields = ('local', 'complemento', 'quantidadev', 'area')


class AvaliacaoVagaSerializer(serializers.ModelSerializer):
    vaga_details = NestedVagasSerializer(source='vaga', read_only=True)
    
    class Meta:
        model = AvaliacaoVaga
        fields = '__all__'

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
        fields = ('id', 'nome', 'acess')

    def get_acess(self, obj):
        filtro_acessibilidades = FiltroAcessibilidade.objects.filter(filtro=obj)
        return [fa.acessibilidade.id for fa in filtro_acessibilidades]


class RespostaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resposta
        fields = '__all__'
