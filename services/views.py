import json
import os
import shutil
import uuid

from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from common.save_files import SaveFiles
from common.tools import extract_pictures, remove_gaps
from services.tasks import save_service_images
from orders.forms import DemandeForm
from orders.models import Demande
from services.models import Category, Service


def home(request):
    if not request.user.is_authenticated:
        return render(request, "signin.html")
    notis = request.user.notification_set.filter(is_read=False).reverse()
    services = Service.objects.select_related("categorie", "artisan").order_by("-rate")[:4]
    Categories = Category.objects.order_by("-id")[:5]
    return render(
        request,
        "home.html",
        {
            "user": request.user,
            "notis": notis,
            "notis_nbr": notis.count(),
            "services": services,
            "Categories": Categories,
        },
    )


class FormValidationForm(forms.Form):
    title = forms.CharField(min_length=3)
    description = forms.CharField(
         widget=forms.Textarea(attrs={
            "rows": 4,
            "placeholder": "Write something...",
            "class": "form-control",
        })
    )
    category = forms.ChoiceField(choices=Service.TYPES_ARTISAN)


def profile(request):
    if request.method == "POST":
        description = request.POST["description"]
        title = request.POST["title"]
        category = request.POST["category"]
        print("my categorie is ", category)
        category = Category.objects.get(id=category)

        service = request.user.service_set.create(
            description=description, title=title, photos="", categorie=category
        )
        service.save()
        files = request.FILES.getlist("files")
        photos = []
        for file in files:
            tmp_name = f"tmp/{uuid.uuid4()}-{remove_gaps(file.name)}"
            tmp_rel = default_storage.save(tmp_name, file)
            photos.append(os.path.join(settings.MEDIA_ROOT, tmp_rel))

        transaction.on_commit(
            lambda: save_service_images.delay(
                service.id, request.user.username, title, photos
            )
        )

        return JsonResponse({"status": "success"})


def services(request):
    user = request.user
    services = list(user.service_set.select_related("categorie"))
    base_url = (
        f"http://{request.META['SERVER_NAME']}:{request.META['SERVER_PORT']}/"
        f"{settings.MEDIA_URL}"
    )
    for service in services:
        service.photos_array = extract_pictures(base_url, service.photos)

    return render(request, "services.html", {"services": services, "user": user})


def modify(request):
    if request.method == "GET" and "id" in request.GET:
        id = request.GET["id"]
        service = Service.objects.select_related("categorie").get(pk=id)
        print(service.description)
        categories = [category[0] for category in Service.TYPES_ARTISAN]
        base_url = (
            f"http://{request.META['SERVER_NAME']}:{request.META['SERVER_PORT']}/"
            f"{settings.MEDIA_URL}"
        )
        imgs = extract_pictures(base_url, service.photos)

        return render(
            request,
            "modify.html",
            {
                "service": service,
                "categories": categories,
                "imgs": imgs,
                "some_value": "Hello from Django!",
            },
        )

    elif request.method == "POST" and "id" in request.POST:
        print(request.POST)
        form = FormValidationForm(request.POST)
        if form.is_valid():
            id = request.POST["id"]
            service = Service.objects.get(pk=id)
            user = request.user

            attrs_to_update = {
                "description": request.POST["description"],
                "title": request.POST["title"],
                "categorie": request.POST["category"],
            }

            media_folder = f"{settings.MEDIA_ROOT}/Service/{user.username}/{service.title}"
            print(f"media folder {media_folder}")
            try:
                if os.path.exists(media_folder):
                    print("Trying to delete:", media_folder)
                    print("Folder exists:", os.path.exists(media_folder))
                    print("Folder is dir:", os.path.isdir(media_folder))
                    shutil.rmtree(media_folder, ignore_errors=True)
                    print("exist")
                else:
                    print("it doesn't exit")
            except Exception as e:
                print("errrrrrrrrrrrrrrrrrrrrrrrrrrrrror")
                print(f"Error deleting folder: {e}")

            files = request.FILES.getlist("photos")
            print(f"the length of list of files is : {len(files)}")
            photos = ""

            for file in files:
                print(type(file))
                name = remove_gaps(file.name)
                SaveFiles().save(file, name, f"Service/{user.username}/{request.POST['title']}")
                photos += f"Service/{user.username}/{request.POST['title']}/{name}*"

            if files:
                attrs_to_update["photos"] = photos

            for attr, value in attrs_to_update.items():
                setattr(service, attr, value)

            service.save()
            print("i am rendering")

            return redirect("service_detail")
        else:
            id = request.POST["id"]
            service = Service.objects.select_related("categorie").get(pk=id)
            categories = [category[0] for category in Service.TYPES_ARTISAN]
            base_url = (
                f"http://{request.META['SERVER_NAME']}:{request.META['SERVER_PORT']}/"
                f"{settings.MEDIA_URL}"
            )
            imgs = extract_pictures(base_url, service.photos)

            return render(
                request,
                "modify.html",
                {
                    "service": service,
                    "categories": categories,
                    "imgs": imgs,
                    "form": form,
                    "errors": form.errors,
                },
            )

    return HttpResponseRedirect(reverse("services"))


def service_detail(request):
    return render(request, "service_detail.html")


def delete(request):
    if request.method == "GET" and "id" in request.GET:
        try:
            id = request.GET["id"]
            service = request.user.service_set.filter(pk=id)
            print(service)
            service.delete()
            return redirect("services")
        except Exception:
            print("there was an error")
            return HttpResponse("<div>there is an error</div>")
    else:
        return HttpResponse("<div>there is an error</div>")


@login_required
def show_service(request):
    services = Service.objects.all()[:9]
    return render(
        request,
        "show_service.html",
        {"services": services, "img": "http://127.0.0.1:8000/media/default.jpg"},
    )


@login_required
@require_POST
def load_services(request):
    print(request.method)
    try:
        data = json.loads(request.body)
        page = int(data.get("page", 1))

        offset = page * 9
        limit = offset + 9

        services = Service.objects.all()[offset:limit]

        total_services = Service.objects.count()
        last_page = (offset + len(services)) >= total_services

        services_data = []
        for service in services:
            services_data.append(
                {
                    "title": service.title,
                    "description": service.description,
                    "image": "http://127.0.0.1:8000/media/default.jpg",
                }
            )

        return JsonResponse(
            {
                "services": services_data,
                "last_page": last_page,
                "message": f"Loaded {len(services_data)} more services",
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def search_filter(request):
    print(request.method)
    data = json.loads(request.body)
    search_query = str(data.get("search_key")).strip()
    keys = search_query.split()
    q_object = Q()
    for key in keys:
        q_object |= (
            Q(title__icontains=key)
            | Q(description__icontains=key)
            | Q(categorie__name__icontains=key)
        )

    result = Service.objects.filter(q_object)

    services_data = []
    for service in result:
        services_data.append(
            {
                "title": service.title,
                "description": service.description,
                "image": "http://127.0.0.1:8000/media/default.jpg",
            }
        )

    return JsonResponse({"services": services_data})


def test(request):
    if request.method == "GET":
        if "key" in request.GET:
            keys = request.GET["key"]

            keys = keys.split()
            q_object = Q()
            for key in keys:
                q_object |= (
                    Q(title__icontains=key)
                    | Q(description__icontains=key)
                    | Q(categorie__name__icontains=key)
                )

            result = Service.objects.filter(q_object)

            paginator = Paginator(result, 20)

            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            print("the length of paginator is ", paginator.count)

            return render(
                request,
                "test.html",
                {
                    "page_obj": page_obj,
                    "keyword": " ".join(keys),
                    "user": request.user,
                    "length": paginator.count,
                },
            )
        else:
            return HttpResponse("<div>matb9ax t9lb f inspect</div>")
    else:
        return HttpResponse("<div>sorry i can't handle it </div>")


def describe_service(request, id):
    form = DemandeForm()
    service = Service.objects.select_related("categorie", "artisan").get(pk=id)
    services = (
        Service.objects.select_related("categorie", "artisan")
        .filter(categorie=service.categorie)
        .exclude(id=id)
    )
    length = len(service.photos.split("*")) - 1
    images = [service.photos.split("*")[i] for i in range(1, length)]
    print("those are my images ", service.photos.split("*"))

    first = services[:6]
    seealso = []
    for x in services:
        seealso.append(
            {
                "photo": x.first.url,
                "title": x.title,
                "description": x.description,
                "categorie": x.categorie.name,
            }
        )
    artisan = service.artisan
    service_set = artisan.service_set.exclude(id=id)
    comments = artisan.owner.select_related("commenter").all()
    print(service_set)
    print(service.first.url)

    return render(
        request,
        "desc_service.html",
        {
            "service": service,
            "images": images,
            "see_also": seealso,
            "more": service_set,
            "first": first,
            "form": form,
            "comments": comments,
            "rates": [1, 2, 3, 4, 5],
            "cities": Demande.cities,
        },
    )


def deleteService(request):
    if request.method == "POST":
        id = request.POST["id"]
        service = Service.objects.get(pk=id)
        service.delete()
        return JsonResponse({"result": "sucess"})


def modifyService(request):
    if request.method == "POST":
        id = request.POST["id"]
        service = Service.objects.get(pk=id)
        user = request.user
        attrs_to_update = {
            "description": request.POST["description"],
            "title": request.POST["title"],
            "categorie": request.POST["category"],
        }

        media_folder = f"{settings.MEDIA_ROOT}/Service/{user.username}/{service.title}"
        print(f"media folder {media_folder}")
        try:
            if os.path.exists(media_folder):
                print("Trying to delete:", media_folder)
                print("Folder exists:", os.path.exists(media_folder))
                print("Folder is dir:", os.path.isdir(media_folder))
                shutil.rmtree(media_folder, ignore_errors=True)
                print("exist")
            else:
                print("it doesn't exit")
        except Exception as e:
            print("errrrrrrrrrrrrrrrrrrrrrrrrrrrrror")
            print(f"Error deleting folder: {e}")

        files = request.FILES.getlist("photos")
        print(f"the length of list of files is : {len(files)}")
        photos = ""

        for file in files:
            print(type(file))
            name = remove_gaps(file.name)
            SaveFiles().save(file, name, f"Service/{user.username}/{request.POST['title']}")
            photos += f"Service/{user.username}/{request.POST['title']}/{name}*"

        if files:
            attrs_to_update["photos"] = photos

            for attr, value in attrs_to_update.items():
                setattr(service, attr, value)

            service.save()
            print("i am rendering")

            return JsonResponse({"result": "sucess"})
