# from django.test import TestCase
#
# # Create your tests here.
# fields=['username','password']
# widgets={'username':forms.TextInput(attrs={'placeholder':'Enter username'}),
        # 'password':forms.TextInput(attrs={'placeholder':'Password'})}
#
# widget={'username':forms.TextInput(attrs={'class':''})
# }
#
# from django.shortcuts import render
# from app1.forms import loginForm
# from app1.models import user
#
#
# # Create your views here.
# def login(request):
#     frm=loginForm
#     err=""
#     if request.method=='POST' and 'sub1' in request.POST:
#         frm=loginForm(request.POST)
#         if frm.is_valid():
#             usr=frm.cleaned_data['username']
#             pss=frm.cleaned_data['password']
#             us,err=checklogin(usr, pss)
#
#             if us==1:
#                 return render(request,'app1/main.html')
#             print(str(us)+" error: "+err)
#             # status,err=checklogin(usr,pss)
#
#             # print("is validate:  "+str(status)+" error:"+err)
#     return render(request,'app1/index.html',{'frm':frm})
#
# def checklogin(usrTxt,pssTxt):
#     validate=0
#     err=""
#     try:
#         us=user.objects.get(username=usrTxt)
#     except user.DoesNotExist:
#         us=None
#     if us is None:
#         print("is none")
#         validate=0
#         err="نام کاربری اشتباه است"
#     else:
#         if us.username==usrTxt:
#             if us.password==pssTxt:
#                 validate=1
#                 print("all correct")
#             else:
#                 print("usr correct but pass is wrong")
#                 validate=0
#                 err="رمز شما اشتباه است"
#     return validate,err
# for creating the new record
q=user(username='ali')
q.save()

from django.core.mail import send_mail
from django.shortcuts import redirect
import random

rnd=random.randint(42587,68541)
print(str(rnd))

from django.shortcuts import render
from app1.forms import loginForm,RegisterForm
from app1.models import user
from django.core.mail import send_mail
from django.shortcuts import redirect
import random

# Create your views here.
def main(request,message):
    return render(request,'app1/main.html',{'message':message})


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
                # return render(request,'app1/main.html',{'message':m})
                return redirect('app1:main',message=m)

            else:
                return redirect('app1:register',msg=m)
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

def Register(request,msg):

    frm2 = RegisterForm
    frm1=loginForm

    t=0
    if request.method=='POST' and 'Sign-up' in request.POST:
        frm2= RegisterForm(request.POST)
        if frm2.is_valid():
            t=checktekarari(frm2.cleaned_data['username'])
            if t==0:
                frm2.save(commit=True)
                msg="با موفقیت ثبت نام کردید"
                # return render(request,'app1/index.html',{'errmessage':err,'frm':frm1})
                return redirect('app1:login')
            else:
                msg="نام کاربری تکراری است"
                return render(request,'app1/SignUp.html',{'errmessage':msg,'frmreg':frm2})

        else:
            msg="خطا دوباره امتحان کنید"
            return render(request,'app1/SignUp.html',{'errmessage':msg,'frmreg':frm2})

    return render(request,'app1/SignUp.html',{'errmessage':msg,'frmreg':frm2})

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

# Email
def sendmail(request):
    frmmail=MailForm

    if request.method=='POST' and 'Recovery' in request.POST:
        frmmail=MailForm(request.POST)
        if frmmail.is_valid():
            mail=frmmail.cleaned_data['email']
            m=checkmail(mail)
            if m==1:
                try:
                    send_mail('Subject',

                    'Email message',
                    'aaamir829@gmail.com',
                    ['aaamir829@gmail.com'],
                    fail_silently=False)
                    return redirect('app1:login',msg="ایمیل خود را چک کنید")

                except Exception as e:

                    return render(request,'app1/PassRecovery.html',{'frmmail':frmmail,'message':"خطای سرور"})


            else:
                return render(request,'app1/PassRecovery.html',{'frmmail':frmmail,'message':"ایمیل مورد نظر وجود ندارد"})

    return render(request,'app1/PassRecovery.html',{'frmmail':frmmail,'message':""})

def checkmail(mailaddress):
    try:
        q=user.objects.get(email=mailaddress)

    except user.DoesNotExist:
        q=None
    if q is None:
        m=0
    else:
        m=1
    return m

# Email settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'aaamir829@gmail.com'
EMAIL_HOST_PASSWORD = '09368200356@'
EMAIL_PORT = 587
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# sendin mail change password
def sendpassword(email):
    try:
        pss=random.randint(456789,987654)
        print(str(pss))
        send_mail('رمز عبور',
        'this is your new password : --->  '+str(pss),
        'aaamir829@gmail.com',
        [email],
        fail_silently=False,)
        q=user.objects.get(email=email)
        q.password=pss
        q.save()
        r="yes"
    except Exception as e:
        r=e

    return r

# emal setting

# MAIL_USE_TLS = True
# MAIL_SERVER= 'smtp.gmail.com'
# MAIL_USERNAME= 'aaamir829@gmail.com'
# MAIL_PASSWORD = '09368200356@'
# MAIL_PORT= 587
EMAIL_USE_TLS=True
EMAIL_HOST='smtp.gmail.com'
EMAIL_HOST_USER='aaamir829'
EMAIL_HOST_PASSWORD='09368200356@'
EMAIL_PORT=587
