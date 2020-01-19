from django.shortcuts import render
from app1.forms import loginForm,RegisterForm,PassForm,flightInfoForm,CompanyForm,TypeForm,delForm
from app1.models import user,typeList,companyList,flight,loggingTable
from django.shortcuts import redirect
from django.core.mail import send_mail
import random
from datetime import datetime,date
import datetime
import openpyxl
import requests
from bs4 import BeautifulSoup
import os
import win32print
from bootstrap_modal_forms.generic import BSModalCreateView,BSModalDeleteView
from django.views.generic import FormView
from app1.mixins import AjaxFormMixin
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_delete,post_save


#saving actions

def save_flight(sender,instance,**kwargs):
    lg=loggingTable(actionName="saved flight record",dateAndTime=datetime.datetime.now())
    lg.save()
    print("logging")

post_save.connect(save_flight,sender=flight)


# formviews Functions
class addFlightFromView(AjaxFormMixin,FormView):
    form_class=flightInfoForm
    template_name='app1/Flight-info-ajax.html'
    success_url='/success/'



#
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
def flightUpdate(request, id):
    try:
        flt = flight.objects.get(pk=id)
    except flight.DoesNotExist:
        raise Http404("flights does not exist")
    if request.method=="POST" and 'updateBtn' in request.POST:
        flt.company=request.POST['company']
        flt.save()
        return redirect('app1:flightlist')


    dp=win32print.GetDefaultPrinter()
    # os.startfile("C:\\Users\\amiri\\Documents\\GitHub\\FlightStrips_django1\\app1\\templates\\app1\\printStrip.html","print")
    # os.startfile(r"C:\Users\amiri\Documents\GitHub\FlightStrips_django1\app1\templates\app1\details.html","print")
    return render(request, 'app1/details.html', {'flt': flt})

def uploadexcel(request):
    excel_data=""
    # if request.method=='POST' and 'btn5' in request.POST:
    #     for row in excel_data:
    #         for cell in row:
    #             flight.objects.create(company=row_data[row][0],
    #                               flightNum=row_data[row][1],
    #                               EOBT=row_data[row][2],
    #                               level=row_data[row][3],
    #                               DesAirport=row_data[row][4],
    #                               route=row_data[row][5],
    #                               dateFrom=row_data[row][6])

    if request.method=='POST' and 'btn4' in request.POST:
        excel_file = request.FILES["excelfile"]
        print(excel_file)

        wb = openpyxl.load_workbook(excel_file)

        worksheet = wb["Sheet1"]
        # print(worksheet["A5"].value)
        print(worksheet)


        excel_data = list()
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                print(type(cell.value))
                row_data.append(str(cell.value))

            print(row_data[2])
            print(row_data[6])
            flight.objects.create(company=row_data[0],
                                  flightNum=row_data[1],
                                  EOBT=row_data[2],
                                  level=row_data[3],
                                  DesAirport=row_data[4],
                                  route=row_data[5],
                                  dateFrom=row_data[6])
                # b.save()
            excel_data.append(row_data)
        # for r in excel_data:
        #     for j in r:
        #         company=str(j.value)
        #         flightNum=str(j.value),
        #                               EOBT=datetime.time(14,5,00),
        #                               level=str(j.value),
        #                               DesAirport=str(j.value),
        #                               route=str(j.value),
        #                               dateFrom=datetime.datetime(2015,5,12))
        # print(excel_data[0][0])

    return render(request,'app1/upload.html',{"excel_data":excel_data})
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


def printStrip(request):
    flt=flight.objects.all()
    return render(request, 'app1/printStrip.html',{'flt':flt})


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

def validate_username(request):
    usr=request.GET.get('username',None)
    data={ 'username_exist':user.objects.filter(username__iexact=usr).exists(),}
    return JsonResponse(data)

def validate_company(request):
    flightNum = request.GET.get('flightNum', None)

    dat = {
        'flightnum_is_taken': flight.objects.filter(flightNum__iexact=flightNum).exists(),}
    return JsonResponse(dat)

def flightinfo(request):
    # check callsign is Excist
    #
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
    cy=""
    tp=""

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
    cy=companyList.objects.all()
    tp=typeList.objects.all()
    return render(request,'app1/main.html',{'frmc':frmc,'frmt':frmt,'msg':msg,'cy':cy,'tp':tp})
def getflightlist(request):
    URL="https://www.digikala.com/product/dkp-1582966/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D9%87%D9%88%D8%A2%D9%88%DB%8C-%D9%85%D8%AF%D9%84-p30-lite-mar-lx1m-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA?variant_id=4272884"
    headers={"agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}
    page=requests.get(URL,headers=headers)
    soup=BeautifulSoup(page.content,'html.parser')
    # flights=soup.prettify()
    # findAll("div", {"class": "stylelistrow"})
    flights=soup.find("div",{"class":"c-product__seller-price-raw js-price-value"}).get_text()
    print(flights)
    return render(request,'app1/getflightlist.html',{'flights':flights})


def PrintPage(request,id):

    flt=flight.objects.get(id=id)

    return render(request,'app1/PrintPage.html',{'flt':flt})

# @login_required
def flightlist(request):
    flights=flight.objects.all()
    company=''
    if request.method=='POST' and 'btn3' in request.POST:
        # company=request.POST['']
        return redirect('app1:printStrip')

    if request.method=='POST' and 'delbtn' in request.POST:
        print(str(request.POST.get('delbtn')))

    if request.method=='GET' and 'srchBtn' in request.GET:
        company=request.GET['company']
        dateFrom=request.GET['datefrom']
        dateTo=request.GET['dateto']
        # the result is between two dates
        try:
            flights=flight.objects.filter(dateFrom__range=(dateFrom,dateTo))
        except flight.DoesNotExist or flights is None:
            flights=flight.objects.all()


    if request.method=='POST' and 'deleteBtn' in request.POST:
        # print(str(request.POST.get('id','f.id')))
        print("btn cancel")


    return render(request,'app1/flightlist.html',{'flights':flights})


# BSModalForm
class delFlight(BSModalDeleteView):
    template_name = 'app1/del.html'
    form_class = delForm
    success_message = 'Success: Book was created.'
    # success_url = reverse_lazy('app1:flightlist')
