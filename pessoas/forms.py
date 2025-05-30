from django import forms
from .models import Pessoa
from .models import Endereco
from .models import FormacaoQualificacao

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = '__all__'
        exclude = ['data_cadastro', 'situacao']
        labels = {
            'cpf': 'CPF',
            'possui_veiculo': 'Possui veículo',
            'email': 'E-mail'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = '__all__'
        exclude = ['pessoa']
        labels = {
            'cep': 'CEP',
            'numero': 'Número'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

class FormacaoQualificacaoForm(forms.ModelForm):
    class Meta:
        model = FormacaoQualificacao
        fields = '__all__'
        exclude = ['pessoa']
        labels = {
            'area_formacao': 'Área de Formação',
            'grau_formacao': 'Grau de Formação',
            'possui_registro_conselho_classe': 'Possui registro de conselho de classe',
            'numero_registro_conselho_classe': 'Número do registro de conselho de classe',
            'text_formacao': 'Caso tenha respondido outros acima, informe sua formação'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
