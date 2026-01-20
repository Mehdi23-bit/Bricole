import json

from django.conf import settings
from django.http import JsonResponse

from django.shortcuts import render
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from common.save_files import SaveFiles
from common.tools import extract_pictures, remove_gaps
from notifications.utils import send_notification_to_user
from orders.forms import DemandeForm
from orders.models import Demande, Notification
from services.models import Category, Service


def ContactArtisan(request):
    if request.method == "POST":
        print(f"i am the user with the id : {request.user.id}")

        url = request.META.get("HTTP_REFERER").split("/")
        id = int(url[-1])

        form = DemandeForm(request.POST)
        if form.is_valid():
            description = request.POST["description"]
            title = request.POST["titre"]
            user = request.user
            files = request.FILES.getlist("photos")
            price = request.POST["price"]
            city = request.POST["city"]
            datetime = request.POST["datetime"]
            photos = ""
            service = Service.objects.get(id=id)
            artisan = service.artisan
            for file in files:
                print(type(file))
                name = remove_gaps(file.name)

                SaveFiles().save(file, name, f"Demande/{user.username}/{title}")
                photos += f"Demande/{user.username}/{title}/{name}*"

            demande = Demande(
                description=description,
                titre=title,
                photos=photos,
                artisan=artisan,
                client=user,
                service=service,
                price=price,
                city=city,
                date=datetime,
            )

            demande.save()

            notification = Notification(owner=demande.artisan, is_read=False, demande=demande)
            notification.save()
            print(f"id is {artisan.id}")
            send_notification_to_user(
                user_id=artisan.id,
                message=demande.description,
                demande_id=demande.id,
                sender=request.user.username,
                title=demande.titre,
                id=demande.id,
                noti_id=notification.id,
            )

            return JsonResponse({"message": "File and data received"})


def mark_as_done(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id = data.get("id")
        print(id)
        notification = Notification.objects.get(pk=id)
        if notification.owner.id == request.user.id:
            notification.is_read = True
            notification.save()
            return JsonResponse({"message": "success"})

    return JsonResponse({"message": "error"})


def dashboard(request):
    def pack_demandes(demandes):
        new_demandes = []
        for demande in demandes:
            imgs = extract_pictures(
                f"http://{request.META['SERVER_NAME']}:{request.META['SERVER_PORT']}{settings.MEDIA_URL}",
                demande.photos,
            )
            print(demande.photos)
            print(imgs)
            new_demandes.append({"demande": demande, "imgs": imgs})
        return new_demandes

    pending_demandes = request.user.demande_artisan_set.select_related(
        "client", "artisan", "service"
    ).filter(status="pending")
    current_demandes = request.user.demande_artisan_set.select_related(
        "client", "artisan", "service"
    ).filter(status="accepted")
    history_demandes = request.user.demande_artisan_set.select_related(
        "client", "artisan", "service"
    ).filter(status="finished")
    declined_demandes = request.user.demande_artisan_set.select_related(
        "client", "artisan", "service"
    ).filter(status="refused")
    new_demandes = pack_demandes(pending_demandes)
    cur_demandes = pack_demandes(current_demandes)
    hist_demandes = pack_demandes(history_demandes)
    dec_demandes = pack_demandes(declined_demandes)
    categories = Category.objects.all()
    services = request.user.service_set.all()
    print("current demandes ", current_demandes)
    return render(
        request,
        "dashboard.html",
        {
            "new_demandes": new_demandes,
            "cur_demandes": cur_demandes,
            "hist_demandes": hist_demandes,
            "dec_demandes": dec_demandes,
            "user": request.user,
            "categories": categories,
            "services": services,
        },
    )


def change_status(request):
    print(request)
    if request.method == "POST":
        print("post")
        id = json.loads(request.body).get("id")
        print("my id is ", id)
        demande = Demande.objects.get(id=int(id))
        demande.status = "accepted"
        demande.save()
        send_notification_to_user(
            user_id=demande.client.id,
            message=f"your demande has been accepted by {demande.artisan.username}",
            demande_id=demande.id,
            sender=request.user.username,
        )
        return JsonResponse({"message": "success"})
    elif request.method == "PATCH":
        print("patch")
        id = json.loads(request.body).get("id")
        demande = Demande.objects.get(id=id)
        demande.status = "refused"
        demande.save()
        send_notification_to_user(
            user_id=demande.client.id,
            message=f"sorry your demande has been declined by {demande.artisan.username}",
            demande_id=demande.id,
            sender=request.user.username,
        )
        return JsonResponse({"message": "success"})
    elif request.method == "PUT":
        print("budweiser")
        id = json.loads(request.body).get("id")

        demande = Demande.objects.get(id=id)
        demande.status = "finished"
        demande.save()
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=30, period=IntervalSchedule.SECONDS
        )

        id_artisan = demande.artisan.id
        id_client = demande.client.id
        task = PeriodicTask.objects.create(
            interval=schedule,
            name=f"{id}/{id_artisan}/{id_client}",
            task="reviews.tasks.comment_notification",
            kwargs=json.dumps(
                {
                    "id": id_client,
                    "demande_id": id,
                    "artisan_username": demande.artisan.username,
                }
            ),
            expires=None,
        )
        task.save()
        send_notification_to_user(
            user_id=demande.client.id,
            message="congrats your service has been done",
            demande_id=demande.id,
            sender=request.user.username,
        )
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "error"})
