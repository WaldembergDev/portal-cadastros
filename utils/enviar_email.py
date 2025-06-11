from django.core.mail import send_mail
from django.conf import settings

def enviar_email(assunto, mensagem, destinatario):
    send_mail(
        assunto,
        mensagem,
        settings.DEFAULT_FROM_EMAIL,
        [destinatario],
        fail_silently=False  #  True para ignorar erros, False para levantar exceção
    )
    return True  # ou False para erros
