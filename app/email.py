from flask_mail import Mail, Message
from flask import render_template
from . import mail

def send_mail(to, subject, template, **kwargs):
  msg = Message(subject, sender='christianyang@wistronits.com', recipients=[to])
  msg.body = render_template(template + '.txt', **kwargs)
  msg.html = render_template(template + '.html', **kwargs)
  mail.send(msg)
