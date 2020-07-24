from celery import shared_task
from django.core.mail import send_mail

@shared_task
def delayed_send_email(to_user, message):
    send_mail(
        'We are testing celery',
        'We are testing celery',
        from_email='contact.nawoka@gmail.com',
        recipient_list=[to_user]
    )
