from smtplib import SMTP
from ssl import create_default_context
from smtplib import SMTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename
from .import_mgr import read_config_as_dict
from .utilities import get_file_extension

settings = read_config_as_dict(app_config=True)["smtp"]


def send_email(subject: str, email_to: str, email_body: str, attached_files: list = None) -> list:
    """
    Sends a plain HTML email.
    :param subject:
    :param email_to:
    :param email_body:
    :param attached_files:
    :return list[bool, status]:
    """
    html_msg = MIMEText(email_body)
    html_msg.set_type('text/html')
    html_msg.set_param('charset', 'UTF-8')

    msg = MIMEMultipart()
    msg.set_type('multipart/alternative')
    msg['Subject'] = subject
    msg['To'] = email_to
    msg['From'] = f'"{settings["from_name"]}"' + f'<{settings["send_from"]}>'
    msg['Reply-To'] = settings["reply_to"]
    msg['Original-Sender'] = settings["username"]
    msg.attach(html_msg)

    for attached_file in attached_files or []:
        with open(attached_file, "rb") as attachment:
            contents = MIMEApplication(attachment.read(), _subtype=get_file_extension(attached_file))
            contents.add_header(
                'content-disposition', 'attachment', filename=basename(attached_file))
        msg.attach(contents)

    try:
        with SMTP(settings["server"], settings["port"]) as connection:
            connection.starttls()
            connection.login(settings["username"], settings["password"])
            connection.sendmail(settings["send_from"], email_to, msg.as_string())
    except SMTPException as error:
        return [False, "AUTHENTICATION OR CONNECTION ISSUE", error]

    return [True, "EMAIL SENT", None]


def test_email_server_connection() -> list:
    """
    Used to test the settings of the smtp settings.
    :return list[bool, status]:
    """
    try:
        ssl_context = create_default_context()
        with SMTP(settings["server"], settings["port"]) as connection:
            connection.starttls(context=ssl_context)
            connection.login(settings["username"], settings["password"])
    except SMTPException as error:
        return [False, "AUTHENTICATION OR CONNECTION ISSUE", error]

    return [True, "ENABLED AND READY", None]
