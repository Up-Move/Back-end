from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from .models import Vagas
from .serializers import VagasSerializer
import json
from django.contrib.gis.measure import D

# Create your views here.

# @permission_classes([AllowAny])
# @permission_classes([IsAuthenticated])
class VagasAPIView(APIView):
    def get(self, request):
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')

        # Crie um objeto Point com base nos parâmetros de latitude e longitude
        point = Point(float(longitude), float(latitude), srid=4326)

        # Realize a consulta filtrando os locais próximos ao ponto
        locais = Vagas.objects.filter(geometry__distance_lte=(point, D(km=1)))
        #locais = Vagas.objects.all()
        # Serialize os objetos retornados
        serializer = VagasSerializer(locais, many=True)

        return Response(serializer.data)

    #cursor = connection.cursor()
    #bbox = (97.82, 30.25, -97.65, 30.29)
    #cursor.execute(
    #    'SELECT ST_AsText(geometry), ST_X(geometry), ST_Y(geometry) FROM "Vagas"')
    #result = cursor.fetchall()

   # json_data = json.dumps(result, default=str)

    #response = HttpResponse(json_data, content_type='application/json')

    #return response