from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings

def send_verification_email(user, request):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account'
    
    # Use frontend URL for verification link
    verification_url = f"{settings.FRONTEND_URL}/verify-email/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}/"
    
    message = render_to_string('accounts/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'verification_url': verification_url,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()


def send_password_reset_email(user, request):
    current_site = get_current_site(request)
    mail_subject = 'Reset your password'
    
    # Use frontend URL for password reset link
    reset_url = f"{settings.FRONTEND_URL}/reset-password/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}/"
    
    message = render_to_string('accounts/password_reset_email.html', {
        'user': user,
        'domain': current_site.domain,
        'reset_url': reset_url,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
