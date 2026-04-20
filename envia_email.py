import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from cria_rel import criar_pdf_rel_manutecao

def conn_smtp():
    return {
        "host" : "smtp.gmail.com",
        "port" : 587,
        "user" : "Seu e-mail",
        "password" : "Senah do app(E-mail)"
    }

def disparar_email(dadosRel):

    arquivo_pdf = criar_pdf_rel_manutecao(dadosRel)

    config = conn_smtp()

    html_msg = """
    <html>
        <body>
            <h2 style="color: #1e3a8a;">Olá, Matheus!</h2>
            <p>O sistema <b>AutoMate</b> gerou o relatório de manutenções programadas.</p>
            <p>Confira os detalhes no arquivo PDF em anexo.</p>
            <br>
            <small>Este é um envio automático.</small>
        </body>
    </html>"""

    msg = MIMEMultipart()
    msg["From"] = config["user"]
    msg["To"] = "mmtavares.slz@gmail.com"
    msg["Subject"] = "Relatório de Próximas Manuteções - AutoMate"

    msg.attach(MIMEText(html_msg, 'html'))

    try:
        with open(arquivo_pdf, "rb") as pdf_file:
            part = MIMEApplication(pdf_file.read(), Name=os.path.basename(arquivo_pdf))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(arquivo_pdf)}"'
            msg.attach(part)
    except Exception as e:
        print(f"Erro ao ler PDF: {e}")

    try:
        smtp = smtplib.SMTP(config["host"], config["port"])
        smtp.starttls()
        smtp.login(config["user"], config["password"])
        smtp.send_message(msg)
        smtp.quit()
    except Exception as e:
        print(f"Erro ao conectar:{e}")