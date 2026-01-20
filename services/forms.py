from .models import Service 
from django import forms
class CreateService(forms.ModelForm):
    photos=forms.ImageField(widget=forms.TextInput(attrs={'id': 'input_images'}))
    class Meta:
        model=Service
        fields=('title','description','photos','categorie')