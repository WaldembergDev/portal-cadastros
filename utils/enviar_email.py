from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from enum import Enum

# definindo os locais do html
class TipoEmail(Enum):
    INSCRICAO = ('emails/inscricao.html', 'Confirmação de inscrição!')
    CADASTRO_APROVADO = ('emails/cadastro_aprovado.html', 'Seu Cadastro Foi Aprovado! Bem-vindo(a) ao Grupo Quality Ambiental')
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
    # defindo as variaveis principais
    assunto = tipo_email.assunto
    remetente = settings.DEFAULT_FROM_EMAIL # Use um e-mail de remetente válido

    # local do html
    template_path =  tipo_email.value

    # 2. Variáveis do template
    context = {
        'nome_usuario': nome_destinatario,
    }

    html_content = render_to_string(template_path, context)

    # Versão em texto puro 
    text_content = f"Olá {context['nome_usuario']}"

    
    message = EmailMultiAlternatives(assunto, text_content, remetente, [email_destinatario])
    message.attach_alternative(html_content, "text/html")

    try:
        message.send()
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")