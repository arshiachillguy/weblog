from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
     email = forms.EmailField()
     class Meta:
          model = User
          fields = ('username' , 'password1' , 'password2' , 'email')

class LoginForm(AuthenticationForm):
     pass

class CreateUserForm(UserCreationForm):
     email = forms.EmailField()
     class Meta:
          model = User
          fields = ('username' , 'password1' , 'password2' , 'email')


class UpdateUserForm(forms.ModelForm):
     class Meta:
          model = User
          fields = ('username' , 'email')
