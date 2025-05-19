from django.db import models
from authentification.models import Users

# Create your models here.
class Comments(models.Model):
    rating=models.IntegerField(default=0)
    comment=models.TextField(max_length=100)
    owner=models.ForeignKey(Users,related_name='owner',on_delete=models.CASCADE) 
    commenter=models.ForeignKey(Users,related_name='commenter',on_delete=models.CASCADE) 
    class Meta:
        db_table='comments'