from django.db import models
import uuid

# Create your models here.
class Pessoa(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False,
                          unique=True)
    nome_completo = models.CharField(max_length=120)
    cpf = models.CharField(max_length=14)
    telefone = models.CharField(max_length=11)
    email = models.CharField(max_length=50)
    possui_veiculo = models.BooleanField()

# dados referente à localização
class Endereco(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False,
                          unique=True)
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=120)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    fornecedor = models.OneToOneField(Pessoa, on_delete=models.CASCADE)