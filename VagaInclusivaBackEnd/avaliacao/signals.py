from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Avaliacao, AvaliacaoVaga


@receiver(post_save, sender=Avaliacao)
def criar_avaliacao_vaga(sender, instance, created, **kwargs):
    if created:
        vaga = instance.vaga
        avaliacao_vaga, _ = AvaliacaoVaga.objects.get_or_create(vaga=vaga)
        avaliacao_vaga.atualizar_media()  # Atualize a média quando uma nova avaliação for criada
