# Generated by Django 5.2.1 on 2025-05-30 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pessoas", "0002_formacaoqualificacao_text_formacao_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="formacaoqualificacao",
            name="area_formacao",
            field=models.CharField(
                choices=[
                    ("Química", "Quimica"),
                    ("Biologia", "Biologia"),
                    ("Meio Ambiente", "Meio Ambiente"),
                    ("Logística", "Logistica"),
                    ("Comercial", "Comercial"),
                    ("Outros", "Outros"),
                ],
                max_length=35,
            ),
        ),
    ]
