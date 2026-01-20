# your_notification_app/utils.py
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_notification_to_user(user_id, message, **extra_data):
     
    """
    Send a notification to a specific user by their ID
    """
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notifications_{user_id}',
        {
            
            'type': 'notification_message',
            'message': message,
            'data': extra_data
        }
    )

def remaind_user(user_id,**extra_data):
    print("ok bro you try  ur best but let's shufle the game an di will remaind you ")
     
    """
    Send a notification to a specific user by their ID
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notifications_{user_id}',
        {
            
            'type': 'remaind_comment',
             
            'data': extra_data
        }
    )

def send_notification_to_users(user_ids, message, **extra_data):
    """
    Send the same notification to multiple users
    """
    channel_layer = get_channel_layer()
    for user_id in user_ids:
        async_to_sync(channel_layer.group_send)(
            f'notifications_{user_id}',
            {
                'type': 'notification_message',
                'message': message,
                'data': extra_data
            }
        )           