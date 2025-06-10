from django.db import models
from pessoas.models import Pessoa
import uuid

class SimNaoEnum(models.TextChoices):
    NAO = 'NAO', 'Não'
    SIM = 'SIM', 'Sim'

class AreaInteresse(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False,
                          unique=True)
    nome = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.nome

# Create your models here.
class Fornecedor(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False,
                          unique=True)
    cnpj = models.CharField(max_length=18, null=True, blank=True)
    nome_empresarial = models.CharField(max_length=120, null=True, blank=True)
    tempo_mei = models.DateField(null=True, blank=True)
    possui_conta_pj = models.CharField(max_length=3, choices=SimNaoEnum.choices) # vinculada ao mei
    cnae_principal = models.CharField(max_length=255, null=True, blank=True)
    cnae_secundario = models.CharField(max_length=255, null=True, blank=True)
    prestou_servicos_mei = models.CharField(max_length=3, choices=SimNaoEnum.choices)
    servicos_prestados = models.TextField(null=True, blank=True)
    area_interesse = models.ManyToManyField(AreaInteresse)
    possui_disponibilidade_servicos_eventuais = models.CharField(max_length=3, choices=SimNaoEnum.choices)
    possui_smartphone = models.CharField(max_length=3, choices=SimNaoEnum.choices)
    atuou_em_laboratorio_analise_ambiental = models.CharField(max_length=3, choices=SimNaoEnum.choices)
    possui_cursos_area_ambiental = models.CharField(max_length=3, choices=SimNaoEnum.choices)
    cursos_realizados = models.CharField(max_length=255, null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True)
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE)
