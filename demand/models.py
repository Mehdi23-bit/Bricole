from django.db import models
from authentification.models import Users
from Services.models import Service 
# Create your models here.

class Demande(models.Model):
    choices=[
        ('pending','PENDING'),
        ('accepted','ACCEPTED'),
        ('refused','REFUSED'),
        ('finished','FINISHED')
    ]
    titre=models.CharField(max_length=30)
    description=models.TextField()
    photos=models.TextField()
    artisan=models.ForeignKey(Users,related_name='artisan',on_delete=models.CASCADE)
    client=models.ForeignKey(Users,related_name='client',on_delete=models.CASCADE)
    service=models.ForeignKey(Service,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=30,choices=choices,default='pending')
    class Meta:
        db_table="demandes"


class Notification(models.Model):
    owner=models.ForeignKey(Users,on_delete=models.CASCADE)
    is_read=models.BooleanField(default=False)
    demande=models.ForeignKey(Demande,on_delete=models.CASCADE)
   
    class Meta:
        db_table="notifications"