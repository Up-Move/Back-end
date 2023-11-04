# Create your views here.
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from .models import Vagas
from .serializers import VagasConversionSerializer
from django.contrib.gis.measure import D
from avaliacao.models import AvaliacaoVaga
from django.db import transaction

# @permission_classes([AllowAny])
# @permission_classes([IsAuthenticated])
class VagasAPIView(APIView):
    def get(self, request):
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')

        point = Point(float(longitude), float(latitude), srid=4326)

        locais = Vagas.objects.filter(geometry__distance_lte=(point, D(km=1)))

        #with transaction.atomic():
        #    for local in locais:
        #        try:
        #            avaliacao_vaga = AvaliacaoVaga.objects.get(vaga_id=local.index)
        #        except AvaliacaoVaga.DoesNotExist:
        #            avaliacao_vaga = AvaliacaoVaga.objects.create(vaga_id=local.index)

        #        local.media_notas = avaliacao_vaga.media_notas
        
        serializer = VagasConversionSerializer(locais, many=True)

        return Response(serializer.data)