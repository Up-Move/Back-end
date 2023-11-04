from avaliacao.models import Acessibilidade

Acessibilidade.create("Calçadas Niveladas")
Acessibilidade.create("Recuo para cadeira lado Direito")
Acessibilidade.create("Recuo para cadeira lado Esquerdo")
Acessibilidade.create("Recuo para cadeira Traseiro")
Acessibilidade.create("Tráfeco local com menor Intensidade")
Acessibilidade.create("Calçadas Largadas")
Acessibilidade.create("Guia Rebaixada")
Acessibilidade.create("Piso Tátil")

# python manage.py shell < tipos_vagas.py
# Manda os Dados para o Banco de Dados