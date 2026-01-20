from django.db import models
from accounts.models import User
from django.conf import settings  

class Category(models.Model):
    name=models.CharField(max_length=255,null=True)    
    photo=models.ImageField()    
    class Meta:
        db_table='categories'

class Service(models.Model):
    

    TYPES_ARTISAN = [
        ('electricien', 'Électricien'),
        ('plombier', 'Plombier'),
        ('macon', 'Maçon'),
        ('carreleur', 'Carreleur'),
        ('peintre', 'Peintre'),
        ('chef_chantier', 'Chef de chantier'),
        ('etancheur', 'Étancheur'),
        ('facadier', 'Façadier'),
        ('plafond_faux', 'Poseur de faux plafonds'),
        ('menuisier', 'Menuisier'),
        ('serrurier', 'Serrurier'),
        ('soudeur', 'Soudeur / Ferronnier'),
        ('vitrier', 'Vitrier'),
        ('technicien_aluminium', 'Technicien aluminium'),
        ('installateur_cuisine', 'Installateur de cuisines'),
        ('installateur_placard', 'Installateur de placards / dressing'),
        ('installateur_gaz', 'Installateur de gaz / chauffe-eau'),
        ('installateur_tv', 'Installateur TV / satellite'),
        ('staffeur', 'Staffeur / Décorateur en plâtre'),
        ('technicien_clim', 'Technicien climatisation / frigo'),
        ('technicien_electromenager', 'Technicien électroménager'),
        ('technicien_info', 'Technicien informatique'),
        ('domoticien', 'Spécialiste domotique / maison intelligente'),
        ('jardinier', 'Jardinier / Paysagiste'),
        ('bricoleur', 'Bricoleur / Multi-travaux'),
        ('nettoyeur', 'Nettoyeur'),
        ('electricien_auto', 'Électricien auto'),
    ]
    
    title=models.CharField(max_length=255,null=True)
    description=models.TextField(null=False)
    first=models.ImageField(upload_to='HeroImage/',default=settings.DEFAULT_SERVICE_HEADER)
    categorie=models.ForeignKey(Category,on_delete=models.CASCADE)
    Note=models.FloatField(default=0)
    artisan=models.ForeignKey(User,on_delete=models.CASCADE)
    rate=models.IntegerField(null=True)
    class Meta:
        db_table='services' 

class Service_Images(models.Model):
    service= models.ForeignKey(Service,on_delete=models.CASCADE)
    image= models.ImageField(upload_to='Service/')

