from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework import status, generics, pagination

from Autenticacao.backends import User
from .models import Avaliacao, Acessibilidade, AvaliacaoAcessibilidade, VagaAcessibilidade, Filtro, \
    FiltroAcessibilidade, Resposta
from .serializers import AvaliacaoSerializer, FiltroSerializer, RespostaSerializer
from rest_framework.views import APIView
from .serializers import AvaliacaoSerializer, AvaliacaoVagaSerializer
from geo.models import Vagas
from django.db.models import F, Count, Avg


class PostAvaliacaoView(RetrieveAPIView):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer

    # atualiza demais VagaAcessibilidade, para ver se ainda estão de acordo
    def check_and_update_threshold(self, vaga_instance):

        total_avaliacoes = vaga_instance.total_avaliacoes
        threshold = total_avaliacoes * 0.30

        to_remove = []  # Create a list to store 'acess' values to remove

        for acessibilidade_id in vaga_instance.acess:
            avaliacao_acess_count = AvaliacaoAcessibilidade.objects.filter(
                accessibilidade_id__id=acessibilidade_id
            ).count()
            if avaliacao_acess_count <= threshold:
                to_remove.append(acessibilidade_id)

            # Remove only if the item is in the list
        for item in to_remove:
            if item in vaga_instance.acess:
                vaga_instance.acess.remove(item)

        # Convert to_remove to a set to remove duplicates
        to_remove_set = set(to_remove)

        # Remove the items from vaga_instance.acess
        vaga_instance.acess = list(set(vaga_instance.acess) - to_remove_set)

        vaga_instance.save()


    def post(self, request):
        serializer = AvaliacaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Atualize a AvaliacaoVaga correspondente
            vaga_id = serializer.validated_data['vaga'].index
            vaga_instance = Vagas.objects.get(index=vaga_id)
            print(vaga_instance.__dict__)

            # Calculate statistics for the related Avaliacao objects
            statistics = Avaliacao.objects.filter(vaga=vaga_instance).aggregate(
                total_avaliacoes=Count('id'),
                media_notas=Avg('nota')
            )

            total_avaliacoes = statistics['total_avaliacoes']
            media_notas = statistics['media_notas']

            vaga_instance.total_avaliacoes = total_avaliacoes
            vaga_instance.media_notas = media_notas
            vaga_instance.save()

            # Check if the threshold is exceeded and update VagaAcessibilidade
            total_avaliacoes = vaga_instance.total_avaliacoes
            threshold = total_avaliacoes * 0.30

            # Criar Acessibilidades
            acessibilidades_data = request.data.get('acess', [])
            for acessibilidade_id in acessibilidades_data:
                try:
                    acessibilidade = Acessibilidade.objects.get(id=acessibilidade_id)
                    AvaliacaoAcessibilidade.objects.create(
                        avaliacao_id=serializer.instance,
                        accessibilidade_id=acessibilidade
                    )

                    # Count the number of AvaliacaoAcessibilidade objects for the Vaga
                    vaga_acess_count = AvaliacaoAcessibilidade.objects.filter(
                        accessibilidade_id=acessibilidade
                    ).count()

                    print(vaga_acess_count)
                    print(threshold)

                    if vaga_acess_count > threshold:
                        # Create or update the VagaAcessibilidade object
                        vaga_instance.acess.append(acessibilidade_id)
                        vaga_instance.save()

                except Acessibilidade.DoesNotExist:
                    pass

            # atualiza demais acessibilidades, deixa tranasação dinâmica
            with transaction.atomic():
                self.check_and_update_threshold(vaga_instance)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAvaliacaoVagaView(APIView):

    def get(self, request, id_vaga):
        vaga, created = Vagas.objects.get_or_create(index=id_vaga)
        serializer = AvaliacaoVagaSerializer(vaga)
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
        id = self.request.query_params.get('vaga_id')
        print(f'first: {first}, last: {last}')

        if id:
            # Filter by vaga_id if provided
            #queryset = queryset.filter(index__index=id)
            queryset = queryset.filter(vaga_id=id)

        if first and last:
            try:
                first = int(first)
                last = int(last)

                if first <= 0 or last <= 0 or first > last:
                    return queryset

                queryset = queryset[first - 1:last]  # Adjust indices since they start from 1
            except ValueError:
                pass

        return queryset


class FiltroAPIView(APIView):
    def post(self, request):
        print(request.data)
        user_email = request.data.get('user')  # Change 'user_id' to 'user_email'
        nome = request.data.get('nome')
        nota = request.data.get('nota')
        acessibilidade_ids = request.data.get('acess', [])

        try:
            User = get_user_model()  # Get the user model dynamically
            user = User.objects.get(email=user_email)  # Change to email lookup
        except User.DoesNotExist:  # Handle the User.DoesNotExist exception
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        filtro, created = Filtro.objects.get_or_create(user=user, nome=nome)

        if not created:
            filtro.delete()
            filtro = Filtro.objects.create(user=user, nome=nome, nota=nota)

        filtro.nota = nota
        filtro.save()

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
        user_email = self.request.query_params.get('email')  # Assuming 'user_email' is passed as a URL parameter
        user = User.objects.get(email=user_email)  # Change to email lookup
        return Filtro.objects.filter(user=user)


class RespostaAPIView(generics.ListCreateAPIView):
    queryset = Resposta.objects.all()
    serializer_class = RespostaSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('user')  # Assuming you receive the email address

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        avaliacao_id = request.data.get('avaliacao')

        try:
            avaliacao = Avaliacao.objects.get(id=avaliacao_id)
        except Avaliacao.DoesNotExist:
            return Response({"error": "Avaliacao not found"}, status=status.HTTP_404_NOT_FOUND)

        comentario = request.data.get('comentario')

        # Create the Resposta object with the user and other data
        resposta = Resposta.objects.create(user=user, avaliacao=avaliacao, comentario=comentario)

        # Increment the 'respostas' variable of the associated 'Avaliacao' object
        avaliacao.respostas += 1
        avaliacao.save()

        serializer = RespostaSerializer(resposta)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get_queryset(self):
        avaliacao_id = self.request.query_params.get('avaliacao_id')
        if avaliacao_id:
            return Resposta.objects.filter(avaliacao__id=avaliacao_id)
        return super().get_queryset()

