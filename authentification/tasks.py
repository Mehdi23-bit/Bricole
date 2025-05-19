from celery import shared_task
from django.core.mail import EmailMessage   
from .utils import send_notification_to_user
@shared_task
def send_email_to_user(id,demande_id):

    email = EmailMessage(
    subject='Rate Your Experience',
    body='<h1>Please rate the job</h1><p>Click here...</p>',
    from_email='your_email@gmail.com',
    to=['elmehdiiskandar3@gmail.com']
)
    email.content_subtype = 'html'  # this makes it HTML
    email.send()
@shared_task
def comment_notification(id,demande_id,artisan_username):

    send_notification_to_user(
                user_id=id,
                message="give us a comment or we gone molest you but please don't send comment so we have reason to molest u ",
                demande_id=demande_id,
                sender=artisan_username,    
                type_notification="harasse"                 
            )
    print("wa 3yiit assat")
