
    <!--main page start here-->
<!-- intial information type and company popup pages -->
<!-- company -->
    <div id="myDIV" class="popup-co" style="display:none;">
      <div class="popup-data">
        <h3> Enter Flight Company name </h3>
        <div class="form-group">
          <label for="usr">Name:</label>
          <input type="text" class="form-control" id="usr"><br>
          <button class="btn btn-success">Send</button>
          <button onclick="Company()" class="btn btn-danger">Close</button>
        </div>
      </div>
    </div>
<!-- flight type -->
    <div id="myDIV2" class="popup-co" style="display:none;">
      <div class="popup-data">
        <h3> Enter Flight type </h3>
        <div class="form-group">
          <label for="usr">Flight type:</label>
          <input type="text" class="form-control" id="usr"><br>
          <button class="btn btn-success">Send</button>
          <button onclick="Cotype()" class="btn btn-danger">Close</button>
        </div>
      </div>
    </div>
<!--end of  intial information type and company popup pages -->
<!-- flight forme -->
<div class="flight-form">
  <h3 style="text-align:center;">Flight information registeration </h3>
  <form method="POST">
    <div class="container">
      <div class="row">
          <!--side 1-->
          <form  method="POST">
            {% csrf_token %}

          <div class="col-md-6 col-sm-6">
              <div class="form-group">
                <label for="sel1">Company:</label>
                <select class="form-control" id="sel1">
                  {% for c in cmp%}
                  <option>{{ c.company }}</option>
                  {% endfor %}
                </select>
              </div>
              <div class="form-group">
                <label for="pwd">Flight Number:</label>
                <!-- <input type="number" class="form-control" id="pwd"> -->
                {{ frm.flightNum }}
              </div>
              <div class="form-group">
                <label for="pwd">Date From:</label>
                <!-- <input type="date" class="form-control" id="pwd"> -->
                <!-- {{ frm.dateFrom }} -->
              </div>
              <div class="form-group">
                <label for="pwd">Date To:</label>
                <!-- <input type="date" class="form-control" id="pwd"> -->
                <!-- {{ frm.dateTo }} -->

              </div>
              <div class="form-group">
                <label for="pwd">EOBT:</label>
                <!-- <input type="time" class="form-control" id="pwd"> -->
                <!-- {{ frm.EOBT }} -->

              </div>
              <div class="form-group">
                <label for="pwd">Dep.Airport:</label>
                {{ frm.DepAirport }}

                <!-- <input type="text" class="form-control" id="pwd"> -->
              </div>
              <div class="form-group">
                <label for="pwd">Des.Airport:</label>
                {{ frm.DesAirport }}

                <!-- <input type="text" class="form-control" id="pwd"> -->
              </div>



              <div class="form-group form-check">
                <label class="form-check-label">
                  <input class="form-check-input" type="checkbox"> Trusted Flight data
                </label>
              </div>
              <!-- <button type="submit" class="btn btn-primary" name="sbt">Submit</button> -->
              <!-- <input type="submit" name="sbt" value="Submit" class="btn btn-primary"> -->
          </div>

          <!-- side 2 -->
          <div class="col-md-6 col-sm-6">
            <div class="form-group">
              <label for="pwd">Level:</label>
              <!-- <input type="text" class="form-control" id="pwd"> -->
              {{ frm.level }}
            </div>
            <div class="form-group">
              <label for="sel1">Type:</label>
              <select class="form-control" id="sel1">
                {% for t in tp %}
                <option>{{ t.Type }}</option>
                 {% endfor %}
              </select>
            </div>
            <div class="form-group">
              <label for="pwd">Route:</label>
              <!-- <input type="text" class="form-control" id="pwd"> -->
              {{ frm.route }}
            </div>
            <div class="form-check">
              <label class="form-check-label">
                <input type="radio" class="form-check-input" name="optradio">Sat
              </label>
            </div>
            <div class="form-check">
              <label class="form-check-label">
                <input type="radio" class="form-check-input" name="optradio">Sun
              </label>
            </div>
            <div class="form-check">
              <label class="form-check-label">
                <input type="radio" class="form-check-input" name="optradio">Mon
              </label>
            </div>
            <div class="form-check">
              <label class="form-check-label">
                <input type="radio" class="form-check-input" name="optradio">Tue
              </label>
            </div>
            <div class="form-check">
              <label class="form-check-label">
                <input type="radio" class="form-check-input" name="optradio">Wed
              </label>
            </div>
            <div class="form-check">
              <label class="form-check-label">
                <input type="radio" class="form-check-input" name="optradio">Thu
              </label>
            </div>
            <div class="form-check">
              <label class="form-check-label">
                <input type="radio" class="form-check-input" name="optradio">Fri
              </label>
            </div>
          </div>
      </div>
    </div>
    <button type="submit" class="btn btn-primary" name="sbt1">Submit</button>

  </form>

</div>
<!-- end flight form -->





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
#initialinfo
# <!-- <button class="dropdown-item" href="{% url 'app1:initialinfo' %}">Flight Company & Type</button> -->
# <a href="{% url 'app1:initialinfo' %}">Company & Type</a>
# end initialinfo
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
