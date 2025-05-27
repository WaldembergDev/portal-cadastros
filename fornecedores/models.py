from django.db import models
import uuid

class AreaFormacaoEnum(models.TextChoices):
    QUIMICA = 'Química'
    BIOLOGIA = 'Biologia'
    MEIO_AMBIENTE = 'Meio Ambiente'
    OUTRA = 'Outra'


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
    cnae_principal = models.CharField()
    cnae_secundario = models.CharField(max_length=255)

class Formacao(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False,
                          unique=True)
    



    

