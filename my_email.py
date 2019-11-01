import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from vars import smtp_server, port, sender_email, password, receiver_email


def send_mail(filename, fname_short):
    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    server = None
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        # TODO: Send email here
        subject = "Pronosports"
        body = "Partidos de la semana."
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        # message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {fname_short}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        server.sendmail(sender_email, receiver_email, text)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        if server is not None:
            server.quit()


def send_mail_fail():
    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    server = None
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        # TODO: Send email here
        subject = "Pronosports"
        body = "Pagina de pronosticos en estado erroneo."
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        # message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        # Add attachment to message and convert message to string
        text = message.as_string()

        # Log in to server using secure context and send email
        server.sendmail(sender_email, receiver_email, text)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        if server is not None:
            server.quit()
