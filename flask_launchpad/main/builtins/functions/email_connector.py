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


def send_email(
        subject: str,
        email_to: str,
        email_body: str,
        attached_files: list = None,
        from_name: str = None,
        send_from: str = None,
        reply_to: str = None,
        username: str = None,
        password: str = None,
        server: str = None,
        port: int = None,
) -> list:
    """
    Sends a plain HTML email.
    """

    if from_name is None:
        from_name = app_config["from_name"]
    if send_from is None:
        send_from = app_config["send_from"]
    if reply_to is None:
        reply_to = app_config["reply_to"]
    if username is None:
        username = app_config["username"]
    if password is None:
        password = app_config["password"]
    if server is None:
        server = app_config["server"]
    if port is None:
        port = app_config["port"]

    html_msg = MIMEText(email_body)
    html_msg.set_type('text/html')
    html_msg.set_param('charset', 'UTF-8')

    msg = MIMEMultipart()
    msg.set_type('multipart/alternative')
    msg['Subject'] = subject
    msg['To'] = email_to
    msg['From'] = f'"{from_name}"' + f'<{send_from}>'
    msg['Reply-To'] = reply_to
    msg['Original-Sender'] = username
    msg.attach(html_msg)

    for attached_file in attached_files or []:
        with open(attached_file, "rb") as attachment:
            contents = MIMEApplication(attachment.read(), _subtype=get_file_extension(attached_file))
            contents.add_header(
                'content-disposition', 'attachment', filename=basename(attached_file))
        msg.attach(contents)

    try:
        with SMTP(server, port) as connection:
            connection.starttls()
            connection.login(username, password)
            connection.sendmail(send_from, email_to, msg.as_string())
    except SMTPException as error:
        return [False, "AUTHENTICATION OR CONNECTION ISSUE", error]

    return [True, "EMAIL SENT", None]


def test_email_server_connection(
        username: str = None,
        password: str = None,
        server: str = None,
        port: str = None,
) -> bool:
    """
    Used to test the settings of the smtp settings.
    """
    if username is None:
        username = app_config["username"]
    if password is None:
        password = app_config["password"]
    if server is None:
        server = app_config["server"]
    if port is None:
        port = app_config["port"]

    try:
        ssl_context = create_default_context()
        with SMTP(server, port) as connection:
            connection.starttls(context=ssl_context)
            connection.login(username, password)
    except SMTPException:
        return False

    return True
