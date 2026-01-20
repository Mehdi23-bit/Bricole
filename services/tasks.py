import os
import shutil

from celery import shared_task
from django.conf import settings

from services.models import Service
from common.tools import remove_gaps


@shared_task
def save_service_images(service_id, username, title, photos):
    service = Service.objects.get(pk=service_id)
    final_dir = os.path.join(settings.MEDIA_ROOT, "Service", username, title)
    os.makedirs(final_dir, exist_ok=True)

    rel_paths = []
    head_photo = None
    for photo in photos:
        name = remove_gaps(os.path.basename(photo))
        dest = os.path.join(final_dir, name)
        if os.path.exists(photo):
            shutil.move(photo, dest)

        rel_path = f"Service/{username}/{title}/{name}"
        if head_photo is None:
            head_photo = rel_path

        rel_paths.append(rel_path)

    service.photos = "*".join(rel_paths)
    service.first = head_photo
    service.save()
