from celery import shared_task
from django.core.mail import EmailMessage   
@shared_task
def send_email_to_user(user_id):

    email = EmailMessage(
    subject='Rate Your Experience',
    body='<h1>Please rate the job</h1><p>Click here...</p>',
    from_email='your_email@gmail.com',
    to=['elmehdiiskandar3@gmail.com']
)
    email.content_subtype = 'html'  # this makes it HTML
    email.send()
