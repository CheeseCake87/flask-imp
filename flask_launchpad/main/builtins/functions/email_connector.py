from smtplib import SMTP
from ssl import create_default_context
from smtplib import SMTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename
from .import_mgr import read_app_config
from .utilities import get_file_extension

app_config = read_app_config(section="smtp")


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
    msg['From'] = f'"{app_config["from_name"]}"' + f'<{app_config["send_from"]}>'
    msg['Reply-To'] = app_config["reply_to"]
    msg['Original-Sender'] = app_config["username"]
    msg.attach(html_msg)

    for attached_file in attached_files or []:
        with open(attached_file, "rb") as attachment:
            contents = MIMEApplication(attachment.read(), _subtype=get_file_extension(attached_file))
            contents.add_header(
                'content-disposition', 'attachment', filename=basename(attached_file))
        msg.attach(contents)

    try:
        with SMTP(app_config["server"], app_config["port"]) as connection:
            connection.starttls()
            connection.login(app_config["username"], app_config["password"])
            connection.sendmail(app_config["send_from"], email_to, msg.as_string())
    except SMTPException as error:
        return [False, "AUTHENTICATION OR CONNECTION ISSUE", error]

    return [True, "EMAIL SENT", None]


def test_email_server_connection() -> bool:
    """
    Used to test the settings of the smtp settings.
    :return list[bool, status]:
    """
    try:
        ssl_context = create_default_context()
        with SMTP(app_config["server"], app_config["port"]) as connection:
            connection.starttls(context=ssl_context)
            connection.login(app_config["username"], app_config["password"])
    except SMTPException:
        return False

    return True
