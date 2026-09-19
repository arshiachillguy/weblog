from django import forms

from .models import post


class InputForm (forms.ModelForm):
     class Meta:
          model = post
          fields = ("title" , "content")