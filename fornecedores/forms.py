from django import forms
from .models import Fornecedor

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = '__all__'
        exclude = ['pessoa']
        widgets = {
            'tempo_mei': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            # Adicione outros widgets aqui se precisar, por exemplo:
            # 'data_outro_campo': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
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
