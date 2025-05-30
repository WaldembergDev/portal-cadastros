from django import forms
from .models import Fornecedor

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = '__all__'
        exclude = ['pessoa']
        widgets = {
            'tempo_mei': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'cnpj': 'CNPJ',
            'tempo_mei': 'Data de Cadastro do MEI',
            'possui_conta_pj': 'Possui conta PJ',
            'cnae_principal': 'CNAE Principal',
            'cnae_secundario': 'CNAE Secundário',
            'prestou_servicos_mei': 'Prestou serviços como MEI',
            'servicos_prestados': 'Serviços Prestados',
            'area_interesse': 'Área(s) de Interesse',
            'possui_disponibilidade_servicos_eventuais': 'Possui disponibilidade para serviços eventuais ou sob demanda',
            'possui_smartphone': 'Possui smartphone com sistema operacional Android para aceite das demandas do trabalho',
            'atuou_em_laboratorio_analise_ambiental': 'Atuou em labotatório de análise ambiental',
            'possui_cursos_area_ambiental': 'Possui cursos na área ambiental',
            'cursos_realizados': 'Caso tenha respondido sim acima, informe os cursos realizados',
            'observacoes': 'Observações - Neste campo coloque informações relevantes que o Grupo Quality precisa saber'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
              # Se já definimos um widget com 'type': 'date', não sobrescreva a classe padrão
            if not (isinstance(field.widget, forms.DateInput) and field.widget.attrs.get('type') == 'date'):
                if isinstance(field.widget, forms.CheckboxInput):
                    field.widget.attrs.update({'class': 'form-check-input'})
                elif not isinstance(field.widget, forms.SelectMultiple): # Para não bagunçar o ManyToManyField
                    field.widget.attrs.update({'class': 'form-control'})
            # Para o ManyToManyField (area_interesse), se quiser classe:
            if isinstance(field.widget, forms.SelectMultiple):
                 field.widget.attrs.update({'class': 'form-select', 'size':'5'}) # Exemplo de classe e tamanho
