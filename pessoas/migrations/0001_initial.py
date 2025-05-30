# Generated by Django 5.2.1 on 2025-05-28 07:30

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('nome_completo', models.CharField(max_length=120)),
                ('cpf', models.CharField(max_length=14)),
                ('telefone', models.CharField(max_length=11)),
                ('email', models.CharField(max_length=50)),
                ('possui_veiculo', models.BooleanField(blank=True, default=False, null=True)),
                ('situacao', models.CharField(choices=[('Pendente', 'Pendente'), ('Analisando', 'Analisando'), ('Aprovado', 'Aprovado'), ('Reprovado', 'Reprovado')], default='Pendente', max_length=50)),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FormacaoQualificacao',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('area_formacao', models.CharField(choices=[('Química', 'Quimica'), ('Biologia', 'Biologia'), ('Meio Ambiente', 'Meio Ambiente'), ('Outros', 'Outros')], max_length=30)),
                ('grau_formacao', models.CharField(choices=[('Técnico', 'Tecnico'), ('Tecnólogo', 'Tecnologo'), ('Graduação', 'Graduacao'), ('Pós-Graduação', 'Pos Graduacao'), ('Mestrado', 'Mestrado'), ('Doutorado', 'Doutorado')], max_length=30)),
                ('possui_registro_conselho_classe', models.CharField(choices=[('Não Possui', 'Nao Possui'), ('CRQ', 'Crq'), ('CRBio', 'Crbio'), ('CREA', 'Crea'), ('Outro', 'Outro')], max_length=30)),
                ('numero_registro_conselho_classe', models.CharField(blank=True, max_length=30, null=True)),
                ('registro_ativo_conselho_classe', models.BooleanField(blank=True, default=False, null=True)),
                ('pessoa', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pessoas.pessoa')),
            ],
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('cep', models.CharField(max_length=9)),
                ('logradouro', models.CharField(max_length=120)),
                ('numero', models.CharField(max_length=10)),
                ('bairro', models.CharField(max_length=50)),
                ('cidade', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=50)),
                ('pessoa', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pessoas.pessoa')),
            ],
        ),
    ]
