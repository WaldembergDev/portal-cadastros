from django.shortcuts import render
from fornecedores.forms import FornecedorForm
from pessoas.forms import PessoaForm
from pessoas.forms import EnderecoForm

# Create your views here
def formulario_cadastro(request):
    if request.method == 'GET':
        fornecedor_form = FornecedorForm()
        pessoa_form = PessoaForm()
        endereco_form = EnderecoForm()
        context = {
            'fornecedor_form': fornecedor_form,
            'pessoa_form': pessoa_form,
            'endereco_form': endereco_form
        }
        return render(request, 'cadastro.html', context=context)
    else:
        pessoa_form = PessoaForm(request.POST)
        endereco_form = EnderecoForm(request.POST)
        fornecedor_form = FornecedorForm(request.POST)
        if pessoa_form.is_valid() and endereco_form.is_valid() and fornecedor_form.is_valid():
            pessoa = pessoa_form.save()
            endereco = endereco_form.save(commit=False)
            fornecedor = fornecedor_form.save(commit=False)
            endereco.pessoa = pessoa
            fornecedor.pessoa = pessoa
            endereco.save()
            fornecedor.save()
            # limpando o formulário após salvar os dados
            pessoa_form = PessoaForm()
            endereco_form = EnderecoForm()
            fornecedor_form = FornecedorForm()
            context = {
                'pessoa_form': pessoa_form,
                'endereco_form': endereco_form,
                'fornecedor_form': fornecedor
            }
