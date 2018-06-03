from flask_mail import Message
from app import mail

def send_email(sender, recipients, text_body, html_body):
    subject = "Group Order Test"
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = "Please Place your order using this link: " + text_body
    #msg.html = '<h1>Please Place your order using this link: <a href ="'+text_body + '"></a></h1>'
    mail.send(msg)
