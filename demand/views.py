# from django.shortcuts import render
# from Services.models import Service
# from .forms import DemandeForm
# from authentification.models import Users
# # Create your views here.


 

# def modify(id,**kwargs):
#     service=Service.objects.get(pk=id)
#     for arg in kwargs.items():
#         setattr(service,arg,kwargs[arg])

#     service.save()    

# def create(request):
#     if request.method == 'POST':
#         form=DemandeForm(request)
#         message= {'message':'error'}
#         if form.is_valid() and 'artisan_id' in request.POST:
#            artisan_id=request.POST['artisan_id']
#            artisan=Users.objects.get(pk=artisan_id)
#            demande=form.save(commit=False)
#            demande.client=request.user
#            demande.artisan=artisan
#            demande.save()
#            message= {'message':'success'}

#         return render(request,'creation.html',message)                

