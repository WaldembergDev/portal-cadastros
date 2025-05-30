from django.db import models
import uuid


# Create your models here.
class Pessoa(models.Model):
    class SituacaoEnum(models.TextChoices):
        PENDENTE = 'Pendente'
        ANALISANDO = 'Analisando'
        APROVADO = 'Aprovado'
        REPROVADO = 'Reprovado'

    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False,
                          unique=True)
    nome_completo = models.CharField(max_length=120)
    cpf = models.CharField(max_length=14)
    telefone = models.CharField(max_length=11)
    email = models.CharField(max_length=50)
    possui_veiculo = models.BooleanField(null=True, blank=True, default=False)
    situacao = models.CharField(max_length=50, choices=SituacaoEnum, default=SituacaoEnum.PENDENTE)
    data_cadastro = models.DateTimeField(auto_now_add=True)

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
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE)

# dados formação
class FormacaoQualificacao(models.Model):
    class AreaFormacaoEnum(models.TextChoices):
        QUIMICA = 'Química'
        BIOLOGIA = 'Biologia'
        MEIO_AMBIENTE = 'Meio Ambiente'
        LOGISTICA = 'Logística'
        COMERCIAL = 'Comercial'
        OUTROS = 'Outros'

    class GrauFormacaoEnum(models.TextChoices):
        TECNICO = 'Técnico'
        TECNOLOGO = 'Tecnólogo'
        GRADUACAO = 'Graduação'
        POS_GRADUACAO = 'Pós-Graduação'
        MESTRADO = 'Mestrado'
        DOUTORADO = 'Doutorado'

    class RegistroConselhoClasseEnum(models.TextChoices):
        NAO_POSSUI = 'Não Possui'
        CRQ = 'CRQ'
        CRBIO = 'CRBio'
        CREA = 'CREA'
        OUTRO = 'Outro'


    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False,
                          unique=True)
    area_formacao = models.CharField(max_length=35, choices=AreaFormacaoEnum.choices)
    text_formacao = models.CharField(null=True, blank=True)
    grau_formacao = models.CharField(max_length=30, choices=GrauFormacaoEnum.choices)
    possui_registro_conselho_classe = models.CharField(max_length=30, choices=RegistroConselhoClasseEnum.choices)
    numero_registro_conselho_classe = models.CharField(max_length=30, null=True, blank=True)
    registro_ativo_conselho_classe = models.BooleanField(null=True, blank=True, default=False)
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE)
