from .models import  Users  
from django.contrib.auth import authenticate
class EmailLogin():
    def authenticate(self,request,email=None,password=None):
        if email is None or password is None:
            email=request.POST['email']
            password=request.POST['password']
        try:
            user=Users.objects.get(email=email)
            username=user.username
            return authenticate(username=username,password=password)
    
        except Users.DoesNotExist:
            return None