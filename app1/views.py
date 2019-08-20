from django.shortcuts import render
from app1.forms import loginForm,RegisterForm,PassForm
from app1.models import user
from django.shortcuts import redirect
from django.core.mail import send_mail
import random


# Create your views here.

def mail(request):
    pssfrm=PassForm
    if request.method=='POST' and 'Recovery' in request.POST:
        pssfrm=PassForm(request.POST)
        if pssfrm.is_valid():
            email=pssfrm.cleaned_data['email']

            m=checkmailexist(email)
            if m==1:
                result=sendpass(email)
                return redirect('app1:login',msg="رمز به ایمیل مورد نظر ارسال شد")
            else:
                return render(request,'app1/PassRecovery.html',{'frm':pssfrm,'message':"ایمیل مورد نظر وجود ندارد"})

    return render(request,'app1/passRecovery.html',{'frm':pssfrm})

def sendpass(emailaddress):
    try:
        newpass=random.randint(456789,987654)
        send_mail('رمز جدید',
        'رمز جدید شما: '+str(newpass),
        'aaamir829@gmail.com',
        [emailaddress],
        fail_silently=False)
        q=user.objects.get(email=emailaddress)
        q.password=newpass
        q.save()
        result=1
    except Exception as e:
        result=0
    return result





def checkmailexist(emailaddress):
    try:
        q=user.objects.filter(email=emailaddress)
    except user.DoesNotExist:
        q=None
    if q.count()<1:
        r=0
    else:
        r=1
    return r
def test(request,message):
    return render(request,'app1/test.html',{'msg':message})

def login(request,msg='d'):
    frm=loginForm
    if msg=='d':
        m=""
    else:
        m=msg
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
    return render(request,'app1/index.html',{'frm':frm,'message':m})

def checklogin(usr,pss):
    validate=0
    err=""
    try:
        q=user.objects.get(username=usr)
    except user.DoesNotExist:
        q=None
    if q is None:
        validate=0
        err="username is not exist or wrong!!!"
    else:
        if q.username==usr:
            if q.password==pss:
                validate=1
                err="you entered successfully!!!"
            else:
                validate=0
                err="username is correct but password is wrong"

    return validate,err

def Register(request):

    frm2 = RegisterForm
    frm1=loginForm
    err=""
    t=0
    if request.method=='POST' and 'Sign-up' in request.POST:
        frm2= RegisterForm(request.POST)
        if frm2.is_valid():
            t=checktekarari(frm2.cleaned_data['username'])
            if t==0:
                frm2.save(commit=True)
                err="با موفقیت ثبت نام کردید"
                # return render(request,'app1/index.html',{'message':err,'frm':frm1})
                return redirect('app1:login',msg=err)

            else:
                err="نام کاربری تکراری است"
                return render(request,'app1/SignUp.html',{'errmessage':err,'frmreg':frm2})

        else:
            err="خطا دوباره امتحان کنید"
            return render(request,'app1/SignUp.html',{'errmessage':err,'frmreg':frm2})

    return render(request,'app1/SignUp.html',{'errmessage':err,'frmreg':frm2})


def checktekarari(usr):
    tek=0
    try:
        u=user.objects.filter(username=usr)
    except user.DoesNotExist:
        u=0
    if u.count()>0:
        tek=1
    else:
        tek=0
    return tek
