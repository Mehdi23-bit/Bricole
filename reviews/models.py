from django.db import models
from accounts.models import User
from services.models import Service

# Create your models here.
class Comments(models.Model):
    rating=models.IntegerField(default=0)
    comment=models.TextField(max_length=100)
    service=models.ForeignKey(Service,on_delete=models.CASCADE ,null=True)
    owner=models.ForeignKey(User,related_name='owner',on_delete=models.CASCADE) 
    commenter=models.ForeignKey(User,related_name='commenter',on_delete=models.CASCADE) 
    class Meta:
        db_table='comments'
