from email import message
import email
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
from utils.api_maps import obter_distancia

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
        return render(request, 'cadastro_fornecedor.html', context=context)
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
            # definindo os dados de distância
            dados_distancia = obter_distancia(endereco.cep)
            if dados_distancia:
                distancia_km = dados_distancia.get('dados_distancia') / 1000 if dados_distancia.get('dados_distancia') else None
                distancia_tempo = dados_distancia.get('dados_tempo')
                endereco.distancia_km = distancia_km
                endereco.distancia_tempo = distancia_tempo
            # salvando os dados
            endereco.save()
            # redirecionando o usuário para a mesma página
            return redirect('/registros/')
        messages.add_message(request, constants.WARNING, 'Erro ao registrar os dados! Tente novamente.')
        return render(request, 'cadastro.html', context=context)


@login_required(login_url='/usuarios/login')
def listar_cadastros(request):
    avaliado = request.GET.get('enviado')
    if avaliado:
        if avaliado == 'true':
            avaliado = True
        else:
            avaliado = False
    else:
        avaliado = False
    cadastros = Pessoa.objects.filter(email_enviado = avaliado)
    context = {
        'cadastros': cadastros
    }
    return render(request, 'listar_cadastros.html', context=context)


@login_required(login_url='/usuarios/login')
def visualizacao_kanban(request):
    pessoas_pendentes = Pessoa.objects.filter(situacao = Pessoa.SituacaoEnum.PENDENTE).filter(email_enviado = False)
    pessoas_aprovadas = Pessoa.objects.filter(situacao = Pessoa.SituacaoEnum.APROVADO).filter(email_enviado = False)
    pessoas_reprovadas = Pessoa.objects.filter(situacao = Pessoa.SituacaoEnum.REPROVADO).filter(email_enviado = False)
    pessoas_concluidas = Pessoa.objects.filter(email_enviado = True)
    context = {
        'pessoas_pendentes': pessoas_pendentes,
        'pessoas_aprovadas': pessoas_aprovadas,
        'pessoas_reprovadas': pessoas_reprovadas,
        'pessoas_concluidas': pessoas_concluidas
    }
    return render(request, 'visualizacao_kanban.html', context=context)


@login_required(login_url="/usuarios/login")
def visualizar_cadastro(request, id):
    pessoa = Pessoa.objects.get(id=id)
    context = {
        'pessoa': pessoa
    }
    return render(request, 'visualizar_cadastro.html', context=context)

@login_required(login_url="/usuarios/login")
def disparar_emails(request):
    # obtendo apenas as pessoas que estão com e-mail - false
    pessoas_pendentes = Pessoa.objects.filter(email_enviado = False)
    # disparando o e-mail para quem está com aprovado
    pessoas_aprovadas = pessoas_pendentes.filter(situacao = Pessoa.SituacaoEnum.APROVADO)
    pessoas_reprovadas = pessoas_pendentes.filter(situacao = Pessoa.SituacaoEnum.REPROVADO)

    # verificando se não existem pessoas classificadas
    if  not pessoas_aprovadas and not pessoas_reprovadas:
        messages.add_message(request, constants.WARNING, 'Não existem pessoas classificadas!')
        return redirect('listar_cadastros')
    for pessoa in pessoas_aprovadas:
        # definindo os dados para enviar o e-amil
        email_destinatario = pessoa.email
        tipo_email = TipoEmail.CADASTRO_APROVADO
        nome_destinatario = pessoa.nome_completo
        # enviando o e-mail
        enviar_email(tipo_email, email_destinatario, nome_destinatario)
        # atualizando o cadastro para mostrar que foi disparado
        pessoa.email_enviado = True
        pessoa.save()
    # disparando o e-mail para quem está reprovado
    for pessoa in pessoas_reprovadas:
        # definindo os dados para enviar o e-amil
        email_destinatario = pessoa.email
        tipo_email = TipoEmail.CADASTRO_REPROVADO
        nome_destinatario = pessoa.nome_completo
        # enviando o e-mail
        enviar_email(tipo_email, email_destinatario, nome_destinatario)
        # atualizando o cadastro para mostrar que foi disparado
        pessoa.email_enviado = True
        pessoa.save()
    
    # retornando o usuário para a mesma página
    pessoas_aprovadas = pessoas_pendentes.filter(situacao = Pessoa.SituacaoEnum.REPROVADO)
    messages.add_message(request, constants.SUCCESS, 'E-mails enviados com sucesso!')
    
    return redirect('listar_cadastros')

@login_required(login_url="/usuarios/login")
def atualizar_cadastro(request, id):
    pessoa = get_object_or_404(Pessoa, id=id)

    action = request.POST.get('action')

    if action == 'aprovar':
        pessoa.situacao = Pessoa.SituacaoEnum.APROVADO
        pessoa.save()
        messages.add_message(request, constants.SUCCESS, 'Cadastro aprovado com sucesso!')
        return redirect('listar_cadastros')
    elif action == 'reprovar':
        pessoa.situacao = Pessoa.SituacaoEnum.REPROVADO
        pessoa.save()
        messages.add_message(request, constants.ERROR, 'Cadastro reprovado com sucesso!')
        return redirect('listar_cadastros')
    else:
        messages.add_message(request, constants.ERROR, 'Erro ao atualizar cadastro!')
    return redirect('visualizar_cadastro', id=id)