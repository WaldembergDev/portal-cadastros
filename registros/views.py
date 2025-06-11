from email import message
from django.shortcuts import redirect, render, get_object_or_404
from fornecedores.forms import FornecedorForm
from pessoas.forms import PessoaForm
from pessoas.forms import EnderecoForm
from pessoas.forms import FormacaoQualificacaoForm
from django.contrib import messages
from django.contrib.messages import constants
from pessoas.models import Pessoa
from django.contrib.auth.decorators import login_required
from utils.enviar_email import enviar_email
from utils.enviar_email import TipoEmail

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
            # definindo os dados para enviar o e-amil
            email_destinatario = pessoa.email
            tipo_email = TipoEmail.INSCRICAO
            nome_destinatario = pessoa.nome_completo
            enviar_email(tipo_email, email_destinatario, nome_destinatario)
            # redirecionando o usuário para a mesma página
            return redirect('/registros/')
        messages.add_message(request, constants.WARNING, 'Erro ao registrar os dados! Tente novamente.')
        return render(request, 'cadastro.html', context=context)


# @login_required(login_url='/usuarios/login')
def listar_cadastros(request):
    cadastros = Pessoa.objects.all()
    context = {
        'cadastros': cadastros
    }
    return render(request, 'listar_cadastros.html', context=context)


# @login_required(login_url='/usuarios/login')
def visualizacao_kanban(request):
    pessoas_pendentes = Pessoa.objects.filter(situacao = Pessoa.SituacaoEnum.PENDENTE)
    pessoas_aprovadas = Pessoa.objects.filter(situacao = Pessoa.SituacaoEnum.APROVADO)
    pessoas_reprovadas = Pessoa.objects.filter(situacao = Pessoa.SituacaoEnum.REPROVADO)
    pessoas_concluidas = Pessoa.objects.filter(situacao = Pessoa.SituacaoEnum.APROVADO)
    context = {
        'pessoas_pendentes': pessoas_pendentes,
        'pessoas_aprovadas': pessoas_aprovadas,
        'pessoas_reprovadas': pessoas_reprovadas,
        'pessoas_concluidas': pessoas_concluidas
    }
    return render(request, 'visualizacao_kanban.html', context=context)


# @login_required(login_url="/usuarios/login")
def visualizar_cadastro(request, id):
    pessoa = Pessoa.objects.get(id=id)
    context = {
        'pessoa': pessoa
    }
    return render(request, 'visualizar_cadastro.html', context=context)

# @login_required(login_url="/usuarios/login")
def disparar_emails(request):
    pessoas_pendentes = Pessoa.objects.filter(email_enviado = False)
    # disparando o e-mail para quem está com aprovado
    pessoas_aprovadas = pessoas_pendentes.filter(situacao = Pessoa.SituacaoEnum.APROVADO.value)
    for pessoa in pessoas_aprovadas:
        # definindo os dados para enviar o e-amil
        email_destinatario = pessoa.email
        tipo_email = TipoEmail.CADASTRO_APROVADO
        nome_destinatario = pessoa.nome_completo
        enviar_email(tipo_email, email_destinatario, nome_destinatario)
    # disparando o e-mail para quem está reprovado
    
    # retornando o usuário para a mesma página
    pessoas_aprovadas = pessoas_pendentes.filter(situacao = Pessoa.SituacaoEnum.REPROVADO.value)
    messages.add_message(request, constants.SUCCESS, 'E-mails enviados com sucesso!')
    
    return redirect('')
    
def atualizar_cadastro(request, id):
    pessoa = get_object_or_404(Pessoa, id=id)

    action = request.POST.get('action')
    print(f'#### {action}')

    if action == 'aprovar':
        pessoa.situacao = Pessoa.SituacaoEnum.APROVADO
        pessoa.save()
        messages.add_message(request, constants.SUCCESS, 'Cadastro aprovado com sucesso!')
    elif action == 'reprovar':
        pessoa.situacao = Pessoa.SituacaoEnum.REPROVADO
        pessoa.save()
        messages.add_message(request, constants.ERROR, 'Cadastro reprovado com sucesso!')
    else:
        messages.add_message(request, constants.ERROR, 'Erro ao atualizar cadastro!')
    return redirect('visualizar_cadastro', id=id)