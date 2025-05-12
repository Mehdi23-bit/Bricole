from faker import Faker
import random
from Services.models import Service
from authentification.models import Users




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
    def handle(self, *args, **kwargs):
        for i in range(200,400):
            username = f"artisan{i}"
            user, _ = Users.objects.get_or_create(username=username, defaults={"password": "test12345"})

        # Assign 3 services to each artisan
            for _ in range(3):
                Service.objects.create(
                artisan=user,
                title=fake.sentence(),
                categorie=random.choice(self.categories)[0],
                description=fake.paragraph(),
                photos="/default.jpg"  
            )
        self.stdout.write(self.style.SUCCESS("Successfully added fake data."))

