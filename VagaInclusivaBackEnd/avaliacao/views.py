from django.conf import settings
from django.db import transaction
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Avaliacao, AvaliacaoVaga, Acessibilidade, AvaliacaoAcessibilidade, VagaAcessibilidade, Filtro, \
    FiltroAcessibilidade, Resposta
from .serializers import AvaliacaoSerializer, FiltroSerializer, RespostaSerializer
from rest_framework.views import APIView
from .serializers import AvaliacaoSerializer, AvaliacaoVagaSerializer
from geo.models import Vagas
from django.db.models import F


class PostAvaliacaoView(RetrieveAPIView):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer

    # atualiza demais VagaAcessibilidade, para ver se ainda estão de acordo
    def check_and_update_threshold(self, vaga_instance):
        total_avaliacoes = AvaliacaoVaga.objects.get(vaga=vaga_instance).total_avaliacoes
        threshold = total_avaliacoes * 0.30

        existing_vaga_acess_objects = VagaAcessibilidade.objects.filter(vaga=vaga_instance)

        vaga_acess_count = AvaliacaoAcessibilidade.objects.filter(
            avaliacao_id__vaga=vaga_instance
        ).count()

        for vaga_acess in existing_vaga_acess_objects:
            if vaga_acess_count <= threshold:
                vaga_acess.delete()
    
    def post(self, request):
        serializer = AvaliacaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Criar Acessibilidades
            acessibilidades_data = request.data.get('acess', [])
            for acessibilidade_id in acessibilidades_data:
                try:
                    acessibilidade = Acessibilidade.objects.get(id=acessibilidade_id)
                    AvaliacaoAcessibilidade.objects.create(
                        avaliacao_id=serializer.instance,
                        accessibilidade_id=acessibilidade
                    )
                except Acessibilidade.DoesNotExist:
                    pass

            # Atualize a AvaliacaoVaga correspondente
            vaga_id = serializer.validated_data['vaga'].index
            vaga_instance = Vagas.objects.get(index=vaga_id)
            avaliacao_vaga, created = AvaliacaoVaga.objects.get_or_create(vaga=vaga_instance)
            avaliacao_vaga.atualizar_media()

            # atualiza demais acessibilidades, deixa tranasação dinâmica
            with transaction.atomic():
                self.check_and_update_threshold(vaga_instance)

            # Check if the threshold is exceeded and update VagaAcessibilidade
            total_avaliacoes = AvaliacaoVaga.objects.get(vaga=vaga_instance).total_avaliacoes
            threshold = total_avaliacoes * 0.30

            # Count the number of AvaliacaoAcessibilidade objects for the Vaga
            vaga_acess_count = AvaliacaoAcessibilidade.objects.filter(
                avaliacao_id__vaga=vaga_instance
            ).count()

            if vaga_acess_count > threshold:
                # Create or update the VagaAcessibilidade object
                vaga_acess, created = VagaAcessibilidade.objects.get_or_create(
                    vaga=vaga_instance,
                    acessibilidade_id=acessibilidade_id
                )
                # Update the current VagaAcessibilidade object
                vaga_acess.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAvaliacaoVagaView(APIView):

    def get(self, request, id_vaga):
        avaliacao_vaga, created = AvaliacaoVaga.objects.get_or_create(vaga_id=id_vaga)
        serializer = AvaliacaoVagaSerializer(avaliacao_vaga)
        status_code = status.HTTP_200_OK if not created else status.HTTP_201_CREATED
        return Response(serializer.data, status=status_code)
    

class AvaliacaoListAPIView(generics.ListAPIView):
    serializer_class = AvaliacaoSerializer

    def get_queryset(self):
        queryset = Avaliacao.objects.annotate(
            recent_order=F('data')
        ).order_by('-recent_order')

        first = self.request.query_params.get('first')
        last = self.request.query_params.get('last')
        vaga_id = self.request.query_params.get('vaga_id')
        print(f'first: {first}, last: {last}')

        if vaga_id:
            # Filter by vaga_id if provided
            queryset = queryset.filter(vaga__index=vaga_id)

        if first and last:
            try:
                first = int(first)
                last = int(last)

                if first <= 0 or last <= 0 or first > last:
                    return Response(
                        {"error": "Invalid 'first' or 'last' values"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                queryset = queryset[first - 1:last]  # Adjust indices since they start from 1
            except ValueError:
                pass
            return Response(
                {"error": "Invalid 'first' or 'last' values"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return queryset


class FiltroAPIView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        nome = request.data.get('nome')
        acessibilidade_ids = request.data.get('acess', [])

        try:
            user = settings.AUTH_USER_MODEL.objects.get(id=user_id)
        except settings.AUTH_USER_MODEL.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        filtro, created = Filtro.objects.get_or_create(user=user, nome=nome)

        if not created:
            return Response({"error": "A filter with the same name already exists for this user."}, status=status.HTTP_400_BAD_REQUEST)

        # Create FiltroAcessibilidade objects
        for acessibilidade_id in acessibilidade_ids:
            try:
                acess = Acessibilidade.objects.get(id=acessibilidade_id)
                FiltroAcessibilidade.objects.create(filtro=filtro, acessibilidade=acess)
            except Acessibilidade.DoesNotExist:
                pass

        return Response(FiltroSerializer(filtro).data, status=status.HTTP_201_CREATED)


class FiltroUserAPIView(generics.ListAPIView):
    serializer_class = FiltroSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']  # Assuming 'user_id' is passed as a URL parameter
        return Filtro.objects.filter(user__id=user_id)


class RespostaAPIView(generics.ListCreateAPIView):
    queryset = Resposta.objects.all()
    serializer_class = RespostaSerializer

    def create(self, request, *args, **kwargs):
        avaliacao_id = request.data.get('avaliacao')
        try:
            avaliacao = Avaliacao.objects.get(id=avaliacao_id)
        except Avaliacao.DoesNotExist:
            return Response({"error": "Avaliacao not found"}, status=status.HTTP_404_NOT_FOUND)

        # Increment the 'respostas' variable of the associated 'Avaliacao' object
        avaliacao.respostas += 1
        avaliacao.save()

        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        avaliacao_id = self.request.query_params.get('avaliacao_id')
        if avaliacao_id:
            return Resposta.objects.filter(avaliacao__id=avaliacao_id)
        return super().get_queryset()

