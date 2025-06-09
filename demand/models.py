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
    cities=[
       ("Casablanca","Casablanca"),
("Fès","Fès"),
("Marrakech","Marrakech"),
("Tangier","Tangier"),
("Sale","Sale"),
("Rabat","Rabat"),
("Meknès","Meknès"),
("Oujda-Angad","Oujda-Angad"),
("Kenitra","Kenitra"),
("Agadir","Agadir"),
("Tétouan","Tétouan"),
("Taourirt","Taourirt"),
("Temara","Temara"),
("Safi","Safi"),
("Khénifra","Khénifra"),
("El Jadid","El Jadid"),
("Laâyoune","Laâyoune"),
("Mohammedia","Mohammedia"),
("Kouribga","Kouribga"),
("Béni Mellal","Béni Mellal"),
("Ait Melloul","Ait Melloul"),
("Nador","Nador"),
("Taza","Taza"),
("Settat","Settat"),
("Barrechid","Barrechid"),
("Al Khmissat","Al Khmissat"),
("Inezgane","Inezgane"),
("Ksar El Kebir","Ksar El Kebir"),
("My Drarga","My Drarga"),
("Larache","Larache"),
("Guelmim","Guelmim"),
("Berkane","Berkane"),
("Ad Dakhla","Ad Dakhla"),
("Bouskoura","Bouskoura"),
("Al Fqih Ben Çalah","Al Fqih Ben Çalah"),
("Oued Zem","Oued Zem"),
("Sidi Slimane","Sidi Slimane"),
("Errachidia","Errachidia"),
("Guercif","Guercif"),
("Oulad Teïma","Oulad Teïma"),
("Ben Guerir","Ben Guerir"),
("Sefrou","Sefrou"),
("Fnidq","Fnidq"),
("Sidi Qacem","Sidi Qacem"),
("Tiznit","Tiznit"),
("Moulay Abdallah","Moulay Abdallah"),
("Youssoufia","Youssoufia"),
("Martil","Martil"),
("Aïn Harrouda","Aïn Harrouda"),
("Souq Sebt Oulad Nemma","Souq Sebt Oulad Nemma"),
("Skhirate","Skhirate"),
("Ouezzane","Ouezzane"),
("Sidi Yahya Zaer","Sidi Yahya Zaer"),
("Al Hoceïma","Al Hoceïma"),
("M’diq","M’diq"),
("Midalt","Midalt"),
("Azrou","Azrou"),
("El Kelaa des Srarhna","El Kelaa des Srarhna"),
("Ain El Aouda","Ain El Aouda"),
("Beni Yakhlef","Beni Yakhlef"),
("Ad Darwa","Ad Darwa"),
("Al Aaroui","Al Aaroui"),
("Qasbat Tadla","Qasbat Tadla"),
("Boujad","Boujad"),
("Jerada","Jerada"),
("Mrirt","Mrirt"),
("El Aïoun","El Aïoun"),
("Azemmour","Azemmour"),
("Temsia","Temsia"),
("Zagora","Zagora"),
("Ait Ourir","Ait Ourir"),
("Aziylal","Aziylal"),
("Sidi Yahia El Gharb","Sidi Yahia El Gharb"),
("Biougra","Biougra"),
("Zaïo","Zaïo"),
("Aguelmous","Aguelmous"),
("El Hajeb","El Hajeb"),
("Zeghanghane","Zeghanghane"),
("Imzouren","Imzouren"),
("Tit Mellil","Tit Mellil"),
("Mechraa Bel Ksiri","Mechraa Bel Ksiri"),
("Al ’Attawia","Al ’Attawia"),
("Demnat","Demnat"),
("Arfoud","Arfoud"),
("Tameslouht","Tameslouht"),
("Bou Arfa","Bou Arfa"),
("Sidi Smai’il","Sidi Smai’il"),
("Souk et Tnine Jorf el Mellah","Souk et Tnine Jorf el Mellah"),
("Mehdya","Mehdya"),
("Aïn Taoujdat","Aïn Taoujdat"),
("Chichaoua","Chichaoua"),
("Tahla","Tahla"),
("Oulad Yaïch","Oulad Yaïch"),
("Moulay Bousselham","Moulay Bousselham"),
("Iheddadene","Iheddadene"),
("Missour","Missour"),
("Zawyat ech Cheïkh","Zawyat ech Cheïkh"),
("Bouknadel","Bouknadel"),
("Oulad Tayeb","Oulad Tayeb"),
("Oulad Barhil","Oulad Barhil"),
("Bir Jdid","Bir Jdid"),
("Tifariti","Tifariti"), 
    ]
    titre=models.CharField(max_length=30)
    description=models.TextField()
    photos=models.TextField()
    artisan=models.ForeignKey(Users,related_name='demande_artisan_set',on_delete=models.CASCADE)
    client=models.ForeignKey(Users,related_name='demande_client_set',on_delete=models.CASCADE)
    service=models.ForeignKey(Service,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=30,choices=choices,default='pending')
    date=models.DateTimeField(null=True)
    price=models.IntegerField(null=True)
    city=models.CharField(max_length=30,choices=cities,default='none')
    class Meta:
        db_table="demandes"


class Notification(models.Model):
    owner=models.ForeignKey(Users,on_delete=models.CASCADE)
    is_read=models.BooleanField(default=False)
    demande=models.ForeignKey(Demande,on_delete=models.CASCADE)
   
    class Meta:
        db_table="notifications"