import json
import time

from django.http import HttpResponse, JsonResponse
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from reviews.models import Comments
from orders.models import Demande


def harasse(request):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=25,
        period=IntervalSchedule.SECONDS,
    )

    task = PeriodicTask.objects.create(
        interval=schedule,
        name=f"slmcv{time.time}",
        task="reviews.tasks.send_email_to_user",
        kwargs=json.dumps({}),
        expires=None,
    )
    task.save()

    return HttpResponse("harasse")


def comment(request):
    if request.method == "POST":
        try:
            comment = json.loads(request.body).get("comment")
            id = json.loads(request.body).get("id")
            rate = json.loads(request.body).get("rate")
            print(f"my rating is {rate}")
            demande = Demande.objects.get(id=id)
            id_artisan = demande.artisan.id
            id_client = demande.client.id
            print(comment, id)
            PeriodicTask.objects.get(name=f"{id}/{id_artisan}/{id_client}").delete()
            commentaire = Comments(
                comment=comment,
                owner=demande.artisan,
                commenter=demande.client,
                rating=rate,
            )
            commentaire.save()
            return JsonResponse({"result": "success"})
        except Exception:
            return JsonResponse({"result": "failled"})
    else:
        return JsonResponse({"result": "failled"})
