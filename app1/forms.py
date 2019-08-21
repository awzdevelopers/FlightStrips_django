from django import forms
from app1.models import user


class loginForm(forms.ModelForm):
    class Meta:
        model=user
        fields=['username','password']
        



class RegisterForm(forms.ModelForm):
    class Meta:
        model=user
        fields=['name','family','username','password','email','phone','job']

class PassForm(forms.ModelForm):
    class Meta:
        model=user
        fields=['email']
