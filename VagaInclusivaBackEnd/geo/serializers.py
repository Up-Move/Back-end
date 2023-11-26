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

    class Meta:
        model = Vagas
        fields = ['latitude', 'longitude', 'index', 'media_notas', 'acess']

    def get_latitude(self, instance):
        latitude = instance.geometry.y
        return latitude

    def get_longitude(self, instance):
        longitude = instance.geometry.x
        return longitude