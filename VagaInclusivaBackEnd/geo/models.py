from django.contrib.gis.db import models
# Create your models here.
# ALTER TABLE "Vagas" ADD CONSTRAINT "unique_index" UNIQUE ("index");

class Vagas(models.Model):
    index = models.BigIntegerField(blank=True, primary_key=True, db_column='index', unique=True)
    numerovaga = models.BigIntegerField(db_column='NumeroVaga', blank=True, null=True)  # Field name made lowercase.
    local = models.TextField(db_column='Local', blank=True, null=True)  # Field name made lowercase.
    complemento = models.TextField(db_column='Complemento', blank=True, null=True)  # Field name made lowercase.
    quantidadev = models.BigIntegerField(db_column='QuantidadeV', blank=True, null=True)  # Field name made lowercase.
    numeroarea = models.BigIntegerField(db_column='NumeroArea', blank=True, null=True)  # Field name made lowercase.
    area = models.TextField(db_column='Area', blank=True, null=True)  # Field name made lowercase.
    tipo = models.TextField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.
    geometry = models.PointField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Vagas'
