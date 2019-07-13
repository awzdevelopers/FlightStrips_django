from django.shortcuts import render
from app1.forms import loginForm
from app1.models import user
from django.core.mail import send_mail

# Create your views here.
def login(request):
    frm=loginForm
    err=""
    if request.method=='POST' and 'sub1' in request.POST:
        frm=loginForm(request.POST)
        if frm.is_valid():

            usr=frm.cleaned_data['username']
            pss=frm.cleaned_data['password']

            s,m=checklogin(usr,pss)
            print(m)

            if s==1:
                return render(request,'app1/main.html',{'message':m})
            else:
                print(m)



    return render(request,'app1/index.html',{'frm':frm})

def checklogin(usr,pss):
    validate=0
    err=""
    try:
        q=user.objects.get(username=usr)
    except user.DoesNotExist:
        q=None
    if q is None:
        validate=0
        err="نام کاربری شما اشتباه هست یا موجود نیست"
    else:
        if q.username==usr:
            if q.password==pss:
                validate=1
                err="شما با موفقیت وارد شدید"
            else:
                validate=0
                err="نام کابری صحیح است اما رمز اشتباه است"

    return validate,err

def sendemail(request):

    send_mail(
        'Subject',
        'Email message',
        'aaamir829@gmail.com',
        ['aaamir829@gmail.com'],
        fail_silently=False,
    )
    return render(request,'app1/mail.html')
