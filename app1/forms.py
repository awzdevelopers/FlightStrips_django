from django import forms
from app1.models import user


class loginForm(forms.ModelForm):
    class Meta:
        model=user
        fields=['username','password']
