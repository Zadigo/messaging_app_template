from celery import shared_task
from django.core.mail import send_mail
from django.template import loader


@shared_task
def send_new_email(to_user, message):
    # send_mail(
    #     'We are testing celery',
    #     'We are testing celery',
    #     from_email='contact.nawoka@gmail.com',
    #     recipient_list=[to_user]
    # )
    print('We are testing Celery')


@shared_task
def send_chat_message(from_user, to_user, message):
    print('Sending chat message')
