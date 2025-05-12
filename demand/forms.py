from django import forms
from .models import Demande

class DemandeForm(forms.ModelForm):
    photos= forms.ImageField()
    class Meta:
        model = Demande
        fields = ['titre', 'description', 'photos']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title of your request'}),
            'decription': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your problem...'}),
            
        }
