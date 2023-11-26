from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Avg, Count
from geo.models import Vagas


# Create your models here.
class Avaliacao(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField()
    nota = models.IntegerField()
    vaga = models.ForeignKey(Vagas, to_field='index', db_column='vaga_id', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='id', on_delete=models.CASCADE)
    respostas = models.IntegerField(default=0)


class AvaliacaoVaga(models.Model):
    vaga = models.ForeignKey(Vagas, to_field='index', db_column='vaga_id', on_delete=models.CASCADE)
    total_avaliacoes = models.PositiveIntegerField(default=0)
    media_notas = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    @classmethod
    def atualizar_media(cls):
        avaliacoes = Avaliacao.objects.values('vaga__index').annotate(
            Count('id'),
            Avg('nota')
        )

        for avaliacao in avaliacoes:
            vaga_id = avaliacao['vaga__index']
            total_avaliacoes = avaliacao['id__count']
            media_notas = avaliacao['nota__avg']

            avaliacao_vaga, created = cls.objects.get_or_create(vaga_id=vaga_id)
            avaliacao_vaga.total_avaliacoes = total_avaliacoes
            avaliacao_vaga.media_notas = media_notas
            avaliacao_vaga.save()


class Acessibilidade(models.Model):
    tipo = models.CharField(max_length=255)

    @classmethod
    def create(cls, tipo):
        acessibilidade = cls(tipo=tipo)
        acessibilidade.save()
        return acessibilidade


class AvaliacaoAcessibilidade(models.Model):
    avaliacao_id = models.ForeignKey(Avaliacao, on_delete=models.CASCADE)
    accessibilidade_id = models.ForeignKey(Acessibilidade, on_delete=models.CASCADE)

class VagaAcessibilidade(models.Model):
    vaga = models.ForeignKey(Vagas, to_field='index', db_column='vaga_id', on_delete=models.CASCADE)
    acessibilidade = models.ForeignKey(Acessibilidade, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('vaga', 'acessibilidade')  # Ensure unique combinations of vaga and acessibilidade

class Filtro(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.TextField()
    nota = models.IntegerField(default=0)

class FiltroAcessibilidade(models.Model):
    filtro = models.ForeignKey(Filtro, on_delete=models.CASCADE)
    acessibilidade = models.ForeignKey(Acessibilidade, on_delete=models.CASCADE)


class Resposta(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE)
    comentario = models.TextField()