from  django.conf import settings
import os    
class SaveFiles():
    def __init__(self):
        pass

    def save(self,file,name,path):
        if not os.path.exists(f"{settings.MEDIA_ROOT}/{path}"):
            os.makedirs(f"{settings.MEDIA_ROOT}/{path}")
        
        with open(f"{settings.MEDIA_ROOT}/{path}/{name}",'wb')as saved_profile:
              saved_profile.write(file.read())
                  
         
         