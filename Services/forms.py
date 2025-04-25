from .models import Services 
from django import forms
class CreateService(forms.ModelForm):
    photos=forms.ImageField()
    class Meta:
        model=Services
        fields=('title','description','photos','categorie')