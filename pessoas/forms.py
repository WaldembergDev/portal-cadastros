from django import forms
from .models import Pessoa
from .models import Endereco
from .models import FormacaoQualificacao

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = '__all__'

class EnderecoForm(forms.ModelForm):
    class meta:
        model = Endereco
        fields = '__all__'
        exclude = ['pessoa']

class FormacaoQualificacaoForm(forms.ModelForm):
    class Meta:
        model = FormacaoQualificacao
        fields = '__all__'
        exclude = ['pessoa']


