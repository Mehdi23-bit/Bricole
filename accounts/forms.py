from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class RegistationForm(UserCreationForm):
    # Only define fields you want to customize
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput()
    )
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "password1", "password2", "avatar")

class LoginForm(forms.ModelForm):
    password=forms.CharField(
        label='Password',
        widget=forms.PasswordInput()
    )        

    class Meta:
        model = User
        fields = ('email', 'password')


class EmailForm(forms.ModelForm):
    email=forms.EmailField()

    class Meta:
        fields=('email',)


class ProfileForm(forms.ModelForm):
    
    class Meta:
        model=User
        fields=("avatar", "email")

class UploadFileForm(forms.Form):
    id = forms.IntegerField()
    file = forms.FileField()        







class UserClient(UserCreationForm):
   
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput()
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','password1','password2')

