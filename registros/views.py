from django.shortcuts import redirect, render
from fornecedores.forms import FornecedorForm
from pessoas.forms import PessoaForm
from pessoas.forms import EnderecoForm
from pessoas.forms import FormacaoQualificacaoForm
from django.contrib import messages
from django.contrib.messages import constants
from pessoas.models import Pessoa
from django.contrib.auth.decorators import login_required

# Create your views here
def formulario_cadastro(request):
    if request.method == 'GET':
        fornecedor_form = FornecedorForm()
        pessoa_form = PessoaForm()
        endereco_form = EnderecoForm()
        formacao_form = FormacaoQualificacaoForm()
        context = {
            'fornecedor_form': fornecedor_form,
            'pessoa_form': pessoa_form,
            'endereco_form': endereco_form,
            'formacao_form': formacao_form,
        }
        return render(request, 'cadastro.html', context=context)
    else:
        pessoa_form = PessoaForm(request.POST)
        endereco_form = EnderecoForm(request.POST)
        fornecedor_form = FornecedorForm(request.POST)
        formacao_form = FormacaoQualificacaoForm(request.POST)
        # verificando se os formulários estão válidos
        if pessoa_form.is_valid() and endereco_form.is_valid() and fornecedor_form.is_valid() and formacao_form.is_valid():
            pessoa = pessoa_form.save()
            endereco = endereco_form.save(commit=False)
            fornecedor = fornecedor_form.save(commit=False)
            formacao = formacao_form.save(commit=False)
            endereco.pessoa = pessoa
            fornecedor.pessoa = pessoa
            formacao.pessoa = pessoa
            endereco.save()
            fornecedor.save()
            fornecedor_form.save_m2m()
            formacao.save()
            # limpando o formulário após salvar os dados
            pessoa_form = PessoaForm()
            endereco_form = EnderecoForm()
            fornecedor_form = FornecedorForm()
            formacao_form = FormacaoQualificacaoForm()
            context = {
                'pessoa_form': pessoa_form,
                'endereco_form': endereco_form,
                'fornecedor_form': fornecedor_form,
                'formacao_form': formacao_form
            }
            messages.add_message(request, constants.SUCCESS, 'Dados registrados com sucesso!')
            return redirect('/registros/')
        messages.add_message(request, constants.WARNING, 'Erro ao registrar os dados! Tente novamente.')
        return render(request, 'cadastro.html', context=context)


@login_required(login_url='/usuarios/login')
def listar_cadastros(request):
    cadastros = Pessoa.objects.all()
    context = {
        'cadastros': cadastros
    }
    return render(request, 'listar_cadastros.html', context=context)