from django.contrib.gis.geos import Point
from rest_framework import serializers
from .models import Vagas
from avaliacao.models import VagaAcessibilidade


class VagasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vagas
        fields = '__all__'


class VagasConversionSerializer(serializers.ModelSerializer):
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    media_notas = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    acess = serializers.SerializerMethodField()  # Add this field
    local = serializers.CharField()
    quantidadeV = serializers.IntegerField(source='quantidadev')
    complemento = serializers.CharField()
    area = serializers.CharField()

    class Meta:
        model = Vagas
        fields = ['latitude', 'longitude', 'index', 'media_notas', 'acess', 'local', 'quantidadeV', 'complemento', 'area']

    def get_latitude(self, instance):
        latitude = instance.geometry.y
        return latitude

    def get_longitude(self, instance):
        longitude = instance.geometry.x
        return longitude
    
    def get_acess(self, instance):
        #Retrieve Acessibilidade IDs for the current Vaga
        vaga_acessibility_ids = VagaAcessibilidade.objects.filter(vaga=instance).values_list('acessibilidade__id',
                                                                                             flat=True)
        #return list(vaga_acessibility_ids)