from threading import Thread

from flask import current_app, Flask
from flask_mail import Message, Attachment

from app import mail


def send_async_email(app: Flask, msg: Message) -> None:
    # requires to recall app context as mail module is not
    # necessarily aware and we need flask-mail module and context
    with app.app_context():
        mail.send(msg)


def send_email(
    subject: str,
    recipients: list[str],
    text_body: str,
    sender: str = None,
    attachments: list[Attachment] = None,
    sync: bool = False,
) -> None:
    """Sends a mail to the designated recipients. By default, sends asynchronously the mail.

    Args:
        - subject: mail subjects
        - recipients: list of email of recipients
        - text_body: the body content of the sent mail
        - sender: defines a sender if this one is different from
        app.config['MAIL_DEFAULT_SENDER']
        - attachments: file to be sent as attachment in mail"""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    if sync:
        mail.send(msg)
    else:
        Thread(
            target=send_async_email, args=(current_app._get_current_object(), msg)
        ).start()
