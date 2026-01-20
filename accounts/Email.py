from .models import  User  
from django.contrib.auth import authenticate
class EmailLogin():
    def authenticate(self,request,email=None,password=None):
        if email is None or password is None:
            email=request.POST['email']
            password=request.POST['password']
        try:
            user=User.objects.get(email=email)
            username=user.username
            return authenticate(username=username,password=password)
    
        except User.DoesNotExist:
            return None