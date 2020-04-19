from django.shortcuts import render
from app1.forms import loginForm,RegisterForm,PassForm,flightInfoForm,CompanyForm,TypeForm,delForm
from app1.models import user,typeList,companyList,flight,loggingTable
from django.shortcuts import redirect
from django.core.mail import send_mail
import random
from datetime import datetime,date,time,timedelta
import datetime
import openpyxl
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from bootstrap_modal_forms.generic import BSModalCreateView,BSModalDeleteView
from django.views.generic import FormView
from app1.mixins import AjaxFormMixin
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_delete,post_save
import os,sys
import win32print
import win32ui
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageWin
from django.db.models import Q
import io
import rx
import time
from django.core import serializers
import threading
from app1.functions import createSquack,sendpass,stripImage,printStripFunction,checktekarariUser,checktekarariEmail

#saving actions
def Flightinfoajax(request):
    return render(request,'app1/Flight-info-ajax.html')
def aj_IDlist(request):
    quer = flight.objects.filter(company='IRA')
    datase = serializers.serialize('json',list(quer))
    data={'datase':datase}
    return JsonResponse(data, safe=False)

def setting(request):
    return render(request,'app1/setting.html')

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



def printStrip(request):
    flt=flight.objects.all()
    return render(request, 'app1/printStrip.html',{'flt':flt})



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

def autoUpdateflightlist(request):
    dd=flight.objects.all()
    sd=serializers.serialize('json',dd)
    return JsonResponse(sd,safe=False)
    # return HttpResponse(flghtlist,content_type='application/json')
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

def checkCallSigh(request):
    flightNum = request.GET.get('company', None)
    flightNum = request.GET.get('flightNum', None)
    flightNum = request.GET.get('dateFrom', None)
    isExist = {
        'callsign_is_taken': flight.objects.filter(company=company,flightNum=flightNum,dateFrom=depDate).exists(),}
    return JsonResponse(isExist)

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
def printing(request):
    dateNow=(datetime.datetime.now()).strftime("%Y")+"-"+(datetime.datetime.now()).strftime("%m")+"-"+(datetime.datetime.now()).strftime("%d")
    timeNow=(datetime.datetime.now()).strftime("%H:%M:%S")
    # timeNow=datetime.datetime.strptime(timeNow,"%H:%M")
    # newTime=timeNow+timedelta(hours=3)
    # +":"+(datetime.datetime.now()).strftime("%M")+":00"
    print("date now is: "+str(dateNow))
    print("time now is: "+str(timeNow))
    print(type(timeNow))
    print(type(dateNow))


    # n=datetime.datetime.(datetime.date.today(),timeNow.time())
    print("<--------")
    # print(n)
    print("-------->")

    q=flight.objects.filter(dateFrom=dateNow)
    if q is None:
        pass
    else:
        for i in q:
            # if i.EOBT>timeNow.time():
            p=datetime.datetime.combine(datetime.date.today(),i.EOBT)
            print("greater.....")
            print("EOBT: "+str(i.EOBT))
            print("timeNow: "+str(timeNow))

            print("diffrent is odf EOBT : "+str(((i.EOBT)-(timeNow))))

        data={'status':True}
    return JsonResponse(data)
def getflightlist(request):
    # source of training
    # https://www.youtube.com/watch?v=fmf_y8zpOgA
    URL="https://www.digikala.com/product/dkp-1582966/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D9%87%D9%88%D8%A2%D9%88%DB%8C-%D9%85%D8%AF%D9%84-p30-lite-mar-lx1m-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA?variant_id=4272884"
    URL2="https://efpl.airport.ir/"


    urlofCaptcha="https://efpl.airport.ir/Login/JpegImage.aspx"

    headers={"agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}
    page=requests.get(urlofCaptcha,headers=headers)
# 2
    # html=urlopen(URL2)
    # s=BeautifulSoup(html.read(),'lxml')
    # print(s.body)
    soup=BeautifulSoup(page.content,'html.parser')
    usename=soup.find('input',id="edUser")


    # soup.find_all(attrs={"class":"img-rounded"})
    # flights=soup.prettify()
    # findAll("div", {"class": "stylelistrow"})
    # flights=soup.find("div",{"class":"c-product__seller-price-raw js-price-value"}).get_text()
    return render(request,'app1/getflightlist.html',{'s':soup,'src':urlofCaptcha,'usr':usename})



def PrintPage(request,id):

    flt=flight.objects.get(id=id)
    stripimage=stripImage(flt)
    successfulrpint=printStripFunction(id)
    if stripImage:
        if successfulrpint:
            print("strip image is created and printed")
        else:
            print("the image is created buuut noot printed!!!!")
    else:
        print("strip image creation error!!!")

    # p=win32print.GetDefaultPrinter()
# 1
    # job=win32print.StartDocPrinter(p,1,("test priniting message",None,"RAW"))
    # win32print.StartPagePrinter(p)
# 1
    # win32print.WritePrinter(p,"1235468foo".encode('utf-8'))
# 1
    # print("job id is: "+str(job))
    # win32print.EndPagePrinter(p)
    # print(win32print.JOB_STATUS_OFFLINE)
# 1
    # print
    return render(request,'app1/PrintPage.html',{'flt':flt})
# def printit():
#     print("threading....")
# @login_required
def retriveData():
    while True:
        print("dataaa")
        time.sleep(2)
    return True
def flightlist(request):
    # threading.Timer(5,printit).start()

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MEDIA_ROOT = os.path.join(BASE_DIR, 'app1','media')
    print(MEDIA_ROOT)

    # image manipulations

    # end of image manipulations

    flights=flight.objects.all()




    company=''
    if request.method=='POST' and 'btn3' in request.POST:
        chk = request.POST.getlist('checked')
        for i in chk:
            print("flight list "+i)
            flt=flight.objects.get(id=i)
            stripImage(flt)
            printStripFunction(i)


        # company=request.POST['']
        # return redirect('app1:printStrip')

    if request.method=='POST' and 'delbtn' in request.POST:
        print(str(request.POST.get('delbtn')))

    if request.method=='GET' and 'srchBtn' in request.GET:
        company=request.GET['company']
        dateFrom=request.GET['datefrom']
        dateTo=request.GET['dateto']
        # the result is between two dates
        try:
            flights=flight.objects.filter(Q(dateFrom__range=(dateFrom,dateTo)) | Q(company=company))
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
