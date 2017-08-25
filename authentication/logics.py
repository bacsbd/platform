import jwt

from datetime import datetime
from django.conf import settings
from django.template import loader
from jinja2 import Template
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site

from authentication.models import User


def send_verification_email(context):
    token = jwt.encode({
        'email': context['email'],
    }, settings.SECRET_KEY, algorithm='HS256')

    token_utf8 = token.decode('utf-8')

    data = {
        'token': token_utf8,
        **context
    }

    body = loader.render_to_string('authentication/email_verification.html', data).strip()

    send_mail(
        subject='Email Address Verification',
        message='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[context['email']],
        html_message=body,
    )



def check_verification(token_utf8):

    token = token_utf8.encode()
    print(token)
    try:
        context = jwt.decode(token, settings.SECRET_KEY)
    except:
        print("token decoding failed")
        return False
    print(context)
    email = context['email']
    user = User.objects.get(email=email)
    print(user)
    if user is None:
        print("Email is not correct")
        return False

    user.verified = True
    user.save()

    return True