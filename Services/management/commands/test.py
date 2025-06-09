from faker import Faker
import random
from Services.models import Service,Category
from authentification.models import Users

from comments.models import Comments


from django.core.management.base import BaseCommand
from faker import Faker


fake = Faker()

class Command(BaseCommand):
    help = "Populate the database with fake data"
    categories =  [
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

    def rand(self):
        i=0
        numbers=[]
        last=-1
        while i<3: 
            
            while True:
                 id=random.randint(0, 79)
                 if id!=last:
                     last=id
                     numbers.append(id)
                     break
            i=i+1;                
        return  numbers         

    def handle(self, *args, **kwargs):
        services=Service.objects.all()
        
        for service in services:
            comments=Comments.objects.filter(service=service)
            print(comments)
            i=0
            rate=0
            for comment in comments:
                i+=1
                rate+=comment.rating
            service.rate=int(rate/i)
            service.save()
        self.stdout.write(self.style.SUCCESS("Successfully added fake data."))



