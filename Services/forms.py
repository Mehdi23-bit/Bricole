from .models import Services 
from django import forms
class CreateService(forms.ModelForm):
    photos=forms.ImageField(widget=forms.TextInput(attrs={'id': 'input_images'}))
    class Meta:
        model=Services
        fields=('title','description','photos','categorie')