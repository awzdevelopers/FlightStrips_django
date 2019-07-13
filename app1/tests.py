from django.test import TestCase

# Create your tests here.
fields=['username','password']
widget={'username':forms.TextInput(attrs={'class' : 'fadeIn second','name':'usrname'}),
        'password':forms.TextInput(attrs={'class' : 'fadeIn third','name':'passwrd'})

widget={'username':forms.TextInput(attrs={'class':''})
}

from django.shortcuts import render
from app1.forms import loginForm
from app1.models import user


# Create your views here.
def login(request):
    frm=loginForm
    err=""
    if request.method=='POST' and 'sub1' in request.POST:
        frm=loginForm(request.POST)
        if frm.is_valid():
            usr=frm.cleaned_data['username']
            pss=frm.cleaned_data['password']
            us,err=checklogin(usr, pss)

            if us==1:
                return render(request,'app1/main.html')
            print(str(us)+" error: "+err)
            # status,err=checklogin(usr,pss)

            # print("is validate:  "+str(status)+" error:"+err)
    return render(request,'app1/index.html',{'frm':frm})

def checklogin(usrTxt,pssTxt):
    validate=0
    err=""
    try:
        us=user.objects.get(username=usrTxt)
    except user.DoesNotExist:
        us=None
    if us is None:
        print("is none")
        validate=0
        err="نام کاربری اشتباه است"
    else:
        if us.username==usrTxt:
            if us.password==pssTxt:
                validate=1
                print("all correct")
            else:
                print("usr correct but pass is wrong")
                validate=0
                err="رمز شما اشتباه است"
    return validate,err
