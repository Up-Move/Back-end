# Create your views here.
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from .models import Vagas
from .serializers import VagasConversionSerializer
from django.contrib.gis.measure import D
from avaliacao.models import AvaliacaoVaga  # Import AvaliacaoVaga model

# @permission_classes([AllowAny])
# @permission_classes([IsAuthenticated])
class VagasAPIView(APIView):
    def get(self, request):
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')

        point = Point(float(longitude), float(latitude), srid=4326)

        locais = Vagas.objects.filter(geometry__distance_lte=(point, D(km=1)))

        #for local in locais:
        #    avaliacao_vaga, created = AvaliacaoVaga.objects.get_or_create(vaga_id=local.index)
        #    local.media_notas = avaliacao_vaga.media_notas
        
        serializer = VagasConversionSerializer(locais, many=True)

        return Response(serializer.data)