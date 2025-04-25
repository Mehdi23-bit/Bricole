from django import forms
from .models import Users
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
        model = Users
        fields = ('first_name', 'last_name', 'email','phone_number','password1','password2','photo')

class LoginForm(forms.ModelForm):
    password=forms.CharField(
        label='Password',
        widget=forms.PasswordInput()
    )        

    class Meta:
        model = Users
        fields = ('email', 'password')


class EmailForm(forms.ModelForm):
    email=forms.EmailField()

    class Meta:
        fields=('email',)


class ProfileForm(forms.ModelForm):
    
    class Meta:
        model=Users
        fields=('photo','email')       

class UploadFileForm(forms.Form):
    username = forms.CharField(max_length=50)
    file = forms.FileField()        