from .utils import send_notification_to_user 
from django.contrib.auth import get_user_model
from demand.models import Demande,Notification
from demand.forms import DemandeForm
from django.shortcuts import render,redirect
from .forms import RegistationForm,LoginForm,EmailForm,ProfileForm,UploadFileForm,UserClient
from django.contrib.auth import  login
from .Email import EmailLogin 
import random
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth import logout
from  django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from .models import Users
from .save_files import SaveFiles
from Services.models import Service
from .tools import remove_gaps,extract_pictures 
from django.http import HttpResponse
from django import forms
import shutil
import os
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import subprocess
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.db.models import Q
# Create your views here.



def sign_client(request):
    form=UserClient()
    if request.method=='POST':
        form=UserClient(request.POST)
        if form.is_valid():
            new_user=form.save(commit=False)
            new_user.username=generate(form.cleaned_data['first_name'],form.cleaned_data['last_name'])
            new_user.save()
            print(new_user.username)
            return redirect("signin")

    return render(request,'signup.html',{'form':form})




#view de signup 
def sign_up(request):
   
    form=RegistationForm()
    if request.method == 'POST':
        form=RegistationForm(request.POST)
        if form.is_valid():
            new_user=form.save(commit=False)
            new_user.username=generate(form.cleaned_data['first_name'],form.cleaned_data['last_name'])
            new_user.role='artisan'
            print(form.cleaned_data['last_name'])
            print(form.cleaned_data['first_name'])
            new_user.save()
            print(new_user.username)
            return redirect("signin")

    return render(request,'join.html',{'form':form})

def home(request):
    if not request.user.is_authenticated:
        return render(request,"signin.html",)
    notis=request.user.notification_set.filter(is_read=False).reverse()
    print(notis)
    return render(request,"home.html",{'user':request.user,'notis':notis,'notis_nbr':notis.count()})

def generate(first_name,last_name):
        charaters=['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', 
 ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~',
 '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        username=f"{random.choice(charaters)}{last_name}{random.choice(charaters)}{first_name}{random.choice(charaters)}"
        return username

#view de sign in
def sign_in(request):
     import sys
     import os

     sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # add current folder to sys.path

     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Bricole.settings")

     import django
     django.setup()

     from django.conf import settings

     print(settings.ALLOWED_HOSTS)

     if request.user.is_authenticated :
          return redirect('home')
     form=LoginForm()
     if request.method=='POST':
          loginEmail=EmailLogin() 
          email=request.POST["email"]
          password=request.POST["password"]  
          user=loginEmail.authenticate(request,email,password)
          if user is not None:
               login(request,user)
               return redirect("home")
          return render(request,'signin.html',{'eror':'there is a problem'})
     return render(request,'signin.html',{'form':form})


def home_page(request):
     if request.user.is_authenticated:
         return redirect("home")
     return render(request,"home_page.html")



def logout_view(request):
     logout(request)
     return redirect("signin")

def sendEmail(request):
     if request.method=='POST':
          email=request.POST['email']
          send_mail(
     "Subject here",
     "Here is the message.",
     "elmehdiiskandar3@gmail.com",
     [f"{email}"],
     fail_silently=False,
     )
          return render(request,'email_form.html',{'success':'you the email is in your inbox check it'})

     return   render(request,'email_form.html')


class FormValidationForm(forms.Form):
    title = forms.CharField(min_length=3)
    description = forms.Textarea()
    category = forms.ChoiceField(choices=Service.TYPES_ARTISAN)
    # photos=forms.FileField()


def profile(request):
  if request.user.is_authenticated:
     if request.method=='POST':
     
         description=request.POST['description']
         title=request.POST['title']
         category=request.POST['category']
         user=Users.objects.get(id=request.user.id)
         files=request.FILES.getlist('files')
         photos=''
         for file in files:
           print(type(file))
           name=remove_gaps(file.name)
                      
           SaveFiles().save(file,name,f"Service/{user.username}/{title}")
           photos+=f"Service/{user.username}/{title}/{name}*"
          
         user=request.user
         service=user.service_set.create(
             description=description,title=title,photos=photos,categorie=category
         )
         print(service.artisan)
         service.save()
     services=[]      
     for category in Service.TYPES_ARTISAN:   
         services.append(category[0])
     return render(request,'create_service.html',{'categories':services})
  else:
       return redirect("signin")
  

def services(request):
    user=request.user
    services=list(user.service_set.all())
    
    for service in services:
        
        service.photos_array=extract_pictures(f"http://{request.META['SERVER_NAME']}:{request.META['SERVER_PORT']}/{settings.MEDIA_URL}",service.photos)
        


    return render(request,'services.html',{'services':services,'user':user})



def modify(request):
    if request.method == 'GET' and 'id' in request.GET:
        id = request.GET['id']
        service = Service.objects.get(pk=id)
        print(service.description)
        categories = []
        for category in Service.TYPES_ARTISAN:
            categories.append(category[0])
        imgs = extract_pictures(f"http://{request.META['SERVER_NAME']}:{request.META['SERVER_PORT']}/{settings.MEDIA_URL}", service.photos)
        
        return render(request, "modify.html", {
            'service': service,
            'categories': categories,
            "imgs": imgs,
            'some_value': 'Hello from Django!',
        })
    
    elif request.method == 'POST' and 'id' in request.POST:
        print(request.POST)
        form = FormValidationForm(request.POST)
        if form.is_valid():
            
            id = request.POST['id']
            service = Service.objects.get(pk=id)
            user = request.user
            
            attrs_to_update = {
                'description': request.POST['description'],  # Note: There's a typo here ('descrition')
                'title': request.POST['title'],
                'category': request.POST['category']
            }
            
            media_folder = f'{settings.MEDIA_ROOT}/Service/{user.username}/{service.title}'
            print(f"media folder {media_folder}")
            try:
                if os.path.exists(media_folder):
                    print("Trying to delete:", media_folder)
                    print("Folder exists:", os.path.exists(media_folder))
                    print("Folder is dir:", os.path.isdir(media_folder))
                    subprocess.run(["rm", "-rf", media_folder])
                    print("exist")
                else:
                    print("it doesn't exit")                    
            except Exception as e:
                print("errrrrrrrrrrrrrrrrrrrrrrrrrrrrror")
                print(f"Error deleting folder: {e}")
            
            files = request.FILES.getlist('photos')
            print(f"the length of list of files is : {len(files)}")
            photos = ''  
            
            for file in files:
                print(type(file))
                name = remove_gaps(file.name)
                SaveFiles().save(file, name, f"Service/{user.username}/{request.POST['title']}")
                photos += f"Service/{user.username}/{request.POST['title']}/{name}*"
            
            
            if files:
                attrs_to_update['photos'] = photos
            
            for attr, value in attrs_to_update.items():
                setattr(service, attr, value)
            
            service.save()
            print("i am rendering")
            
            return redirect('service_detail')
        else:
            id = request.POST['id']
            service = Service.objects.get(pk=id)
            categories = []
            for category in Service.TYPES_ARTISAN:
                categories.append(category[0])
            imgs = extract_pictures(f"http://{request.META['SERVER_NAME']}:{request.META['SERVER_PORT']}/{settings.MEDIA_URL}", service.photos)
            
            return render(request, "modify.html", {
                'service': service,
                'categories': categories,
                'imgs': imgs,
                'form': form,
                'errors': form.errors
            })
    
    # Handle all other cases - when neither of the above conditions are met
    return HttpResponseRedirect(reverse('services_list'))  # Or redirect to an appropriate page
        
def service_detail(request):
    return render(request,'service_detail.html')        

def delete(request):
    if request.method == 'GET' and 'id' in request.GET:
        try:
            id=request.GET['id']
            service=request.user.service_set.filter(pk=id)
            print(service)
            service.delete()
            return redirect('services')
        except:
            print("there was an error")
            return HttpResponse("<div>there is an error</div>") 
    else:
        return HttpResponse("<div>there is an error</div>")     

# views.py


@login_required
def show_service(request):
    """View to render the initial services page"""
    # Get first 9 services for initial page load
    services = Service.objects.all()[:9]
    return render(request, 'show_service.html', {'services': services,'img':"http://127.0.0.1:8000/media/default.jpg"})

@login_required
@require_POST
def load_services(request):
    print(request.method)
    """AJAX view to load more services with pagination"""
    try:
        data = json.loads(request.body)
        page = int(data.get('page', 1))
        
        # Calculate offset and limit
        offset = page * 9  # 9 items per page
        limit = offset + 9
        
        # Get services for requested page
        services = Service.objects.all()[offset:limit]
        
        # Check if this is the last page
        total_services = Service.objects.count()
        last_page = (offset + len(services)) >= total_services
        
        # Prepare services data for JSON response
        services_data = []
        for service in services:
            services_data.append({
                'title': service.title,
                'description': service.description,
                'image': 'http://127.0.0.1:8000/media/default.jpg',
            })
        
        return JsonResponse({
            'services': services_data,
            'last_page': last_page,
            'message': f'Loaded {len(services_data)} more services'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def search_filter(request):
        
    # try:
        print(request.method)
        data=json.loads(request.body)
        search_query=str(data.get('search_key')).strip()
        keys=search_query.split()
        q_object=Q()
        for key in keys:
            q_object |= Q(title__icontains=key) | Q(description__icontains=key)    | Q(categorie__icontains=key)  

        result=Service.objects.filter(q_object)    

        services_data = []
        for service in result:
            services_data.append({
                'title': service.title,
                'description': service.description,
                'image': 'http://127.0.0.1:8000/media/default.jpg',
            })
        
        return JsonResponse({
            'services': services_data
            })
    # except Exception as e:
    #     return JsonResponse({'error': str(e),}, status=400)
                


from django.core.paginator import Paginator


def test(request):
    # Get the list of objects (e.g., all products or results)
    if request.method=='GET':
        if 'key' in request.GET: 
            keys=request.GET['key']
        
            keys=keys.split()
            q_object=Q()
            for key in keys:
                q_object |= Q(title__icontains=key) | Q(description__icontains=key)    | Q(categorie__icontains=key)  

            result=Service.objects.filter(q_object)  

            # Create a paginator with 10 items per page
            paginator = Paginator(result, 10)  # Show 10 objects per page

            # Get the current page number from the request (default to 1 if not specified)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            

            return render(request, 'test.html', {'page_obj': page_obj,'keyword':key,'user':request.user})
        else:
            return HttpResponse('<div>matb9ax t9lb f inspect</div>')
    else:

        return HttpResponse("<div>sorry i can't handle it </div>")


def describe_service(request,id):
        form=DemandeForm()
        service=Service.objects.get(pk=id)
        services=Service.objects.filter(categorie=service.categorie).exclude(id=id)
        first=services[:6]
        seealso=[]
        for x in services:
            seealso.append({'photo':'http://127.0.0.1:8000/media/default.jpg'
                            ,'title':x.title,
                            'description':x.description,
                            'categorie':x.categorie})
        artisan=service.artisan
        service_set=artisan.service_set.exclude(id=id)
        print(service_set)
        return render(request,'desc_service.html',{'service':service,'see_also':seealso,'more':service_set,'first':first,'form':form})

def ContactArtisan(request):
    if request.method=='POST':
   
    
       
       url=request.META.get('HTTP_REFERER').split('/')
       id=int(url[-1])
    
       form =DemandeForm(request)
       if form.is_valid:
         
         description=request.POST['description']
         title=request.POST['titre']
         user=request.user
         files=request.FILES.getlist('photos')
         photos=''
         service=Service.objects.get(id=id)
         artisan=service.artisan
         for file in files:
           print(type(file))
           name=remove_gaps(file.name)
                      
           SaveFiles().save(file,name,f"Demande/{user.username}_{artisan.username}/{title}")
           photos+=f"Demande/{user.username}/{title}/{name}*"
          
         
         demande=Demande(
             description=description,titre=title,photos=photos,artisan=artisan,client=user,service=service
         )
         
         demande.save()
         
         User = get_user_model()
         notification=Notification(owner=demande.artisan,is_read=False,demande=demande)
         notification.save()
         print(f'id is {artisan.id}') 
         send_notification_to_user(
                user_id=artisan.id,
                message=demande.description,
                demande_id=demande.id,
                sender=request.user.username,
                title=demande.titre,
                id=demande.id,
                noti_id=notification.id
               
            )
                    
         return JsonResponse({'message': 'File and data received'})
    
def mark_as_done(request):
    if request.method=='POST':
        data = json.loads(request.body)
        id = data.get('id')
        print(id)
        notification=Notification.objects.get(pk=id)
        if notification.owner.id==request.user.id:
            notification.is_read=True
            notification.save()   
            return JsonResponse({"message":"success"})  
                   
    
    return JsonResponse({"message":"error"})  
            

def dashboard(request):
    user_demandes=Demande.objects.filter(artisan_id=request.user.id)
    print(user_demandes)
    return render(request,"dashboard.html",{"demandes":user_demandes})     
   

     