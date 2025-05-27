from django import forms
from .models import Fornecedor

class FronecedorForm(forms.ModelForm):
    class meta:
        model = Fornecedor
        fields = '__all__'
        exclude = ['pessoa']
