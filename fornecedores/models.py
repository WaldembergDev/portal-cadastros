from django.db import models
from pessoas.models import Pessoa
import uuid

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
    cnpj = models.CharField(max_length=18)
    nome_empresarial = models.CharField(max_length=120)
    tempo_mei = models.DateField()
    possui_conta_pj = models.BooleanField() # vinculada ao mei
    cnae_principal = models.CharField(max_length=255)
    cnae_secundario = models.CharField(max_length=255)
    prestou_servicos_mei = models.BooleanField()
    servicos_prestados = models.TextField()
    area_interesse = models.ManyToManyField(AreaInteresse)
    possui_disponibilidade_servicos_eventuais = models.BooleanField()
    possui_smartphone = models.BooleanField()
    atuou_em_laboratorio_analise_ambiental = models.BooleanField()
    possui_cursos_area_ambiental = models.BooleanField()
    cursos_realizados = models.CharField(max_length=255, null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True)
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE)
