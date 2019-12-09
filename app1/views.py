from django.shortcuts import render
from app1.forms import loginForm,RegisterForm,PassForm,flightInfoForm,CompanyForm,TypeForm
from app1.models import user,typeList,companyList,flight
from django.shortcuts import redirect
from django.core.mail import send_mail
import random
import datetime


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

def login(request,msg='default'):
    frm=loginForm
    if msg=='default':
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
                return redirect('app1:flightlist')
                # return render(request,'app1/main.html',{'username':m})
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
def flightinfo(request):
    week_days= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
    dateDiff=''
    msg=''
    flightfrm=flightInfoForm
    cmp=companyList.objects.all()
    tp=typeList.objects.all()
    name='aaaa'
    e=''
    count=0
    day=""
    print("loading post.....")

    if request.method=='POST' and 'sbt' in request.POST:
        flightfrm=flightInfoForm(request.POST)
        print("loading flightfrm.....")
        # dates
        date1=request.POST.get("dateFrom")
        date2=request.POST.get("dateTo")
        print("date1 : "+str(date1))
        print("date2 : "+str(date2))
        l1=list(map(int, date1.split('/')))
        l2=list(map(int, date2.split('/')))
        print("splitting..."+str(l1))
        print("splitting..."+str(l2))

        dateFr = datetime.date(l1[2],l1[0],l1[1])
        dateT = datetime.date(l2[2],l2[0],l2[1])
        dateDiff=dateT-dateFr
        if (dateDiff.days>0 or dateDiff.days==0):
            print("> 0 or == 0" +"days:"+str(dateDiff.days))
            # end dates
            # do saving
            if flightfrm.is_valid():
                print("checking the validation....")
                for i in range((dateT -dateFr).days+1):
                    print("number of day "+str(i))
                    dateFrom=dateFr + datetime.timedelta(days=i)
                    print("current processing date: "+str(dateFrom))
                    daysselcted=request.POST.getlist('daysOfweek')
                    if week_days[dateFrom.weekday()] in daysselcted:
                        count=count+1
                        day=week_days[dateFrom.weekday()]
                        print(str(i)+" date:....>"+str(dateFrom)+"  daysofweek:...>"+week_days[dateFrom.weekday()])
                        print("****start saving the "+str(dateFrom)+" days of week....>"+week_days[dateFrom.weekday()])
                        # flightfrm.level=request.POST.get("level")
                        # flightfrm.company = request.POST.get("company")

                        print("before saving ...."+str(flightfrm.cleaned_data['dateTo']))
                        instance=flightfrm.save(commit=False)
                        print("in instance saving-----"+str(day))
                        instance.daysOfweek=day
                        instance.dateFrom=dateFrom
                        instance.dateTo=dateFrom
                        instance.delay=False
                        instance.pk=None
                        instance.save()
                        print("****end saving the "+str(dateFrom)+" days of week....>"+week_days[dateFrom.weekday()])

                # for i in range(0,count):
                #     instance.pk=None
                #     instance.save()

                    # if week_days[day]==daysselcted[0]:
                    #     print('correct.....')

                    # this date diff
                    # for i in range((dateT -dateFr).days + 1):
                    #     print(dateFr + datetime.timedelta(days=i))
                    # e=calculateDateDay(flightfrm.dateFrom,flightfrm.dateTo,daysselcted)
                    # end of



                    # for day in daysselcted:
                    #     print("saving....."+day)
        else:
            msg="تارخ دوم از تارخ اول کوچک تر است!!!"

        msg=str(count)+" = "+" تعداد پروازهای ثبت شده"

    return render(request,'app1/flight-info.html',{'frm':flightfrm,'name':name,'cmp':cmp,'tp':tp,'msg':msg})

def Register(request):

    frm2 = RegisterForm
    frm1=loginForm
    err=""
    t1=0
    t2=0
    if request.method=='POST' and 'Sign-up' in request.POST:
        frm2= RegisterForm(request.POST)
        if frm2.is_valid():
            t1=checktekarariUser(frm2.cleaned_data['username'])
            t2=checktekarariEmail(frm2.cleaned_data['email'])
            if t1==0:
                if t2==0:

                    frm2.save(commit=True)
                    err="با موفقیت ثبت نام کردید"
                    # return render(request,'app1/index.html',{'message':err,'frm':frm1})
                    return redirect('app1:login',msg=err)

                else:
                    err="ایمیل تکراری است"
                    return render(request,'app1/SignUp.html',{'errmessage':err,'frmreg':frm2})
            else:
                err="نام کاربری تکراری است"
                return render(request,'app1/SignUp.html',{'errmessage':err,'frmreg':frm2})
        else:
            err="خطا دوباره امتحان کنید"
            return render(request,'app1/SignUp.html',{'errmessage':err,'frmreg':frm2})

    return render(request,'app1/SignUp.html',{'errmessage':err,'frmreg':frm2})


def checktekarariUser(usr):
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
def checktekarariEmail(email):
    tek=0
    try:
        u=user.objects.filter(email=email)
    except user.DoesNotExist:
        u=0
    if u.count()>0:
        tek=1
    else:
        tek=0
    return tek
def main(request):
    frmc=CompanyForm
    frmt=TypeForm
    msg=""

    if request.method=='POST' and 'btncompany' in request.POST:
        frmc=CompanyForm(request.POST)
        if frmc.is_valid():
            frmc.save(commit=True)
            msg="با موفقیت انجام شد"
    if request.method=='POST' and 'btntype' in request.POST:
        frmt=TypeForm(request.POST)
        if frmt.is_valid():
            frmt.save(commit=True)
            msg="با موفقیت انجام شد"

    return render(request,'app1/main.html',{'frmc':frmc,'frmt':frmt,'msg':msg})
def flightlist(request):
    flights=flight.objects.all()
    if request.method=='POST' and 'btn3' in request.POST:
        print("iterating...."+flight.objects.get(company=="ira"))



    return render(request,'app1/flightlist.html',{'flights':flights})
