from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
import requests
from PIL import Image
from Bricole.settings import MEDIA_ROOT
import os

class CustomedAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        print("=== DEBUGGING SOCIAL LOGIN ===")
        
        # Debug: Print all available data (safely)
        extra_data = sociallogin.account.extra_data
        print(f"Full extra_data: {extra_data}")
        
        # Try to get email from different sources
        email_from_extra_data = extra_data.get('email')
        print(f"Email from extra_data: {email_from_extra_data}")
        
        # Check sociallogin.user safely
        try:
            if hasattr(sociallogin, 'user') and sociallogin.user:
                print(f"Existing user email: {sociallogin.user.email}")
        except:
            print("No existing user found")
        
        # Call parent method
        user = super().save_user(request, sociallogin, form)
        print(f"User after save_user: {user}")
        print(f"User email after save_user: {user.email}")
        
        # If email is None, manually set it
        if not user.email and email_from_extra_data:
            print(f"Setting email manually: {email_from_extra_data}")
            user.email = email_from_extra_data
            user.save()
            print(f"Email after manual save: {user.email}")
        
        # Download and save profile picture
        picture_url = extra_data.get("picture")
        if picture_url:
            try:
                response = requests.get(picture_url)
                response.raise_for_status()
                
                user_dir = os.path.join(MEDIA_ROOT, 'profile')
                os.makedirs(user_dir, exist_ok=True)
                
                file_path = os.path.join(user_dir, f'{user.username}.jpg')
                
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                
                user.avatar = f"profile/{user.username}.jpg"
                user.save()
                
                print(f"Profile picture saved for user: {user.email}")
                
            except requests.RequestException as e:
                print(f"Error downloading profile picture: {e}")
            except Exception as e:
                print(f"Error saving profile picture: {e}")
        
        print("=== END DEBUGGING ===")
        return user

    def populate_user(self, request, sociallogin, data):
        """
        Override this method to ensure email is properly populated
        This is called before save_user
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Force email from extra_data if not set
        extra_data = sociallogin.account.extra_data
        if not user.email and extra_data.get('email'):
            user.email = extra_data.get('email')
            print(f"Email set in populate_user: {user.email}")
        
        return user
