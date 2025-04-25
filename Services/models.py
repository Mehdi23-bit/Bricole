from django.db import models
from authentification.models import Users

class Services(models.Model):
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
    title=models.CharField(max_length=30,null=True)
    description=models.TextField(null=False)
    photos=models.CharField(max_length=100)
    categorie=models.CharField(max_length=30,choices=TYPES_ARTISAN)
    Note=models.FloatField()
    artisan=models.ForeignKey(Users,on_delete=models.CASCADE)
    class Meta:
        db_table='services'