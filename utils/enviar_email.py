from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from enum import Enum
import requests
import json

# definindo os locais do html
class TipoEmail(Enum):
    INSCRICAO = ('emails/inscricao.html', 'Confirmação de inscrição!')
    CADASTRO_APROVADO = ('emails/cadastro_aprovado.html', 'Seu Cadastro Foi Aprovado!')
    CADASTRO_REPROVADO = ('emails/cadastro_reprovado.html', 'Atualização do seu Cadastro - Grupo Quality Ambiental')

    @property
    def template_path(self):
        """Retorna o caminho do template HTML associado ao tipo de e-mail."""
        return self.value[0]

    @property
    def assunto(self):
        """Retorna o assunto padrão associado ao tipo de e-mail."""
        return self.value[1]



def enviar_email(tipo_email: TipoEmail, email_destinatario: str, nome_destinatario: str):
    # Definindo as variáveis principais
    assunto = tipo_email.assunto
    
    # Remetente: o nome do remetente pode ser fixo ou vir de uma setting
    # A ZeptoMail usa 'address' para o email e 'name' para o nome do remetente
    remetente_email = settings.DEFAULT_FROM_EMAIL 
    remetente_nome = "Grupo Quality Ambiental" # Ou de uma setting, ex: settings.EMAIL_FROM_NAME

    # Local do html (corrigido para usar a propriedade template_path)
    template_path = tipo_email.template_path

    # Variáveis do template
    context = {
        'nome_usuario': nome_destinatario,
    }

    html_content = render_to_string(template_path, context)

    # Versão em texto puro
    text_content = f"Olá {context['nome_usuario']}"

    # --- Configurações da API ZeptoMail ---
    api_key = settings.ZEPTOMAIL_API_KEY
    api_endpoint = settings.ZEPTOMAIL_API_ENDPOINT

    # Verificação básica para chaves da API
    if not api_key:
        print("Erro: ZEPTOMAIL_API_KEY não configurada nas settings.")
        return
    if not api_endpoint:
        print("Erro: ZEPTOMAIL_API_ENDPOINT não configurada nas settings.")
        return

    headers = {
        'Accept': "application/json",
        'Content-Type': "application/json",
        # Use sua chave Zoho aqui, o formato é 'Zoho-enczapikey SEU_API_KEY'
        # Confirme este cabeçalho na documentação da ZeptoMail para sua API.
        'Authorization': f"Zoho-enczapikey {api_key}",
    }

    # Estrutura do payload (corpo da requisição JSON) para a ZeptoMail
    # Adapte conforme a documentação EXATA da ZeptoMail para o endpoint de envio.
    payload = {
        "from": {
            "address": remetente_email,
            "name": remetente_nome
        },
        "to": [
            {
                "email_address": { # A documentação da ZeptoMail usa um dicionário com 'email_address'
                    "address": email_destinatario,
                    "name": nome_destinatario
                }
            }
        ],
        "subject": assunto,
        "htmlbody": html_content,
        "textbody": text_content,
        # Você pode adicionar outras opções aqui como 'track_clicks', 'track_opens', 'tags', etc.
        # Consulte a documentação da ZeptoMail para todas as opções disponíveis.
    }

    try:
        # A requisição POST para a API da ZeptoMail
        response = requests.post(api_endpoint, headers=headers, data=json.dumps(payload))
        
        # Levanta um erro se o status da resposta for 4xx ou 5xx
        response.raise_for_status() 

        # Se tudo ocorreu bem, imprima a resposta da API (útil para depuração)
        print("E-mail enviado com sucesso!")
        print(f"Resposta da API ZeptoMail: {response.json()}")

    except requests.exceptions.RequestException as e:
        # Captura erros relacionados à requisição HTTP (conexão, timeouts, etc.)
        print(f"Erro ao enviar e-mail via API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Detalhes da resposta da API (código {e.response.status_code}): {e.response.text}")
        else:
            print("Não foi possível obter detalhes da resposta da API.")
    except Exception as e:
        # Captura outros erros genéricos que possam ocorrer
        print(f"Ocorreu um erro inesperado: {e}")