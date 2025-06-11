from django.db import models
import uuid

class SimNaoEnum(models.TextChoices):
    NAO = 'NAO', 'Não'
    SIM = 'SIM', 'Sim'


# Create your models here.
class Pessoa(models.Model):
    class SituacaoEnum(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        APROVADO = 'APROVADO', 'Aprovado'
        REPROVADO = 'REPROVADO', 'Reprovado'
        CONCLUIDO = 'CONCLUIDO', 'Concluído'

    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False,
                          unique=True)
    nome_completo = models.CharField(max_length=120)
    cpf = models.CharField(max_length=14)
    telefone = models.CharField(max_length=11)
    email = models.CharField(max_length=50)
    possui_veiculo = models.CharField(max_length=3, choices=SimNaoEnum.choices)
    situacao = models.CharField(max_length=50, choices=SituacaoEnum.choices, default=SituacaoEnum.PENDENTE)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    email_enviado = models.BooleanField(default=False)

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
    distancia_km = models.IntegerField(null=True, blank=True)
    distancia_tempo = models.CharField(max_length=255, null=True, blank=True)
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE)

# dados formação
class FormacaoQualificacao(models.Model):
    class AreaFormacaoEnum(models.TextChoices):
        QUIMICA = 'QUIMICA', 'Química'
        BIOLOGIA = 'BIOLOGIA', 'Biologia'
        MEIO_AMBIENTE = 'MEIO_AMBIENTE', 'Meio Ambiente'
        LOGISTICA = 'LOGISTICA', 'Logística'
        COMERCIAL = 'COMERCIAL', 'Comercial'
        OUTROS = 'OUTROS', 'Outros'

    class GrauFormacaoEnum(models.TextChoices):
        ENSINO_MEDIO = 'ENSINO_MEDIO', 'Ensino Médio'
        TECNICO = 'TECNICO', 'Técnico'
        TECNOLOGO = 'TECNOLOGO', 'Tecnólogo'
        GRADUACAO = 'GRADUACAO', 'Graduação'
        POS_GRADUACAO = 'POS_GRADUACAO', 'Pós-Graduação'
        MESTRADO = 'MESTRADO', 'Mestrado'
        DOUTORADO = 'DOUTORADO', 'Doutorado'

    class RegistroConselhoClasseEnum(models.TextChoices):
        NAO_POSSUI = 'NAO_POSSUI', 'Não Possui'
        CRQ = 'CRQ', 'CRQ'
        CRBIO = 'CRBIO', 'CRBio'
        CREA = 'CREA', 'CREA'
        OUTRO = 'OUTRO', 'Outro'


    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False,
                          unique=True)
    area_formacao = models.CharField(max_length=35, choices=AreaFormacaoEnum.choices)
    text_formacao = models.CharField(null=True, blank=True)
    grau_formacao = models.CharField(max_length=30, choices=GrauFormacaoEnum.choices)
    possui_registro_conselho_classe = models.CharField(max_length=30, choices=RegistroConselhoClasseEnum.choices)
    numero_registro_conselho_classe = models.CharField(max_length=30, null=True, blank=True)
    registro_ativo_conselho_classe = models.CharField(max_length=3, choices=SimNaoEnum.choices)
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE)
