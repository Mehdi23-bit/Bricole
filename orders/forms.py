from django import forms
from .models import Demande

class DemandeForm(forms.ModelForm):
   
    class Meta:
        model = Demande
        fields = ['titre', 'description']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title of your request'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your problem...'}),
            
        }
