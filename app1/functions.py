import os,sys
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageWin
from app1.models import flight,user
import win32ui,win32print
# sqauck function
def createSquack(tarikh):
    i=0
    squacks=["6350","6351","6352","6353","6354","6355",
    "6356","6357","6360","6361","7101","7102","7103","7104","7105","7106","7107"]


    for s in squacks:
        if flight.objects.filter(squack__iexact=s,dateFrom=tarikh).exists():
            print("tekrari "+s)
        else:
            newsquack=s
            break


    # ss=squacks.pop(i)
    # if flight.objects.filter(squack__iexact=ss).exists():
    #     for b in len(squacks):
    #         print("the "+newsquack+" is exsit")
    #         i=i+1
    #         if i>len(squacks)-1:
    #             i=0
    #             newsquack=squacks.pop(i)
    #             break
    #         else:
    #             newsquack=squacks.pop(i)
    #             break
    # else:
    #     newsquack=ss

    # squacks=squacks.remove[0]
    # print("new squack "+newsquack)
    print("new squack "+newsquack)
    return newsquack
# check email exists
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
# password
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

# check user tekrari
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

# check email tekrari
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
# strip image
def stripImage(fltData):
    # the image folder directory
    try:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        MEDIA_ROOT = os.path.join(BASE_DIR,'app1','media')
        dateOfflight=fltData.dateFrom.strftime("%Y-%m-%d")
        print("the date of flight is : "+dateOfflight)
        squa=createSquack(fltData.dateFrom)
        print("stripimage method: "+squa)
        # loading data of flight by id
        baseimage=Image.open(BASE_DIR+r'\app1\static\image\stripD.jpg','r').convert('RGB')
        # newimg=Image.new('RGB',baseimage.size,(255,255,255))
        # baseimage.rotate(90)
        fnt=ImageFont.truetype('arial.ttf',50)
        d=ImageDraw.Draw(baseimage)
        d.text((90,5),fltData.DesAirport,font=fnt,fill=(0,0,0))
        if fltData.change==True:
            d.line((350,35,450,35),fill=128,width=5)
            d.text((350,5),fltData.type,font=fnt,fill=(0,0,0))
            d.text((350,50),fltData.typeChange,font=fnt,fill=(0,0,0))
        else:
            d.text((350,5),fltData.type,font=fnt,fill=(0,0,0))
        d.text((130,120),fltData.company,font=fnt,fill=(0,0,0))
        d.text((230,120),fltData.flightNum,font=fnt,fill=(0,0,0))
        if fltData.delay==True:
            d.line((500,80,700,80),fill=128,width=5)
            d.text((500,50),str(fltData.EOBT),font=fnt,fill=(0,0,0))
            d.text((500,95),str(fltData.EOBTrevision),font=fnt,fill=(0,0,0))
        else:
            d.text((500,50),str(fltData.EOBT),font=fnt,fill=(0,0,0))
        d.text((1000,50),fltData.level,font=fnt,fill=(0,0,0))
        d.text((750,220),fltData.route,font=fnt,fill=(0,0,0))
        d.text((90,200),squa,font=fnt,fill=(0,0,0))
        # baseimage.save(MEDIA_ROOT+fltData.company+fltData.flightNum+".jpg")
        # rotate
        # baseimage.rotate(90).save(MEDIA_ROOT+r"\DEPstrip{}".format(fltData.company+fltData.flightNum+".jpg"))
        # convert to garyscale color
        # baseimage.convert(mode="l").save(MEDIA_ROOT+r"\DEPstrip{}".format(fltData.company+fltData.flightNum+".jpg"))
        # filter image,eg:gaussianblur,....
        # baseimage.filter(ImageFilter.gaussianblur(15)).save(MEDIA_ROOT+r"\DEPstrip{}".format(fltData.company+fltData.flightNum+".jpg"))

        baseimage.save(MEDIA_ROOT+r"\DEPstrip{}".format(fltData.company+fltData.flightNum+"-"+dateOfflight+".jpg"))
        # fltData.stripImage=('/absolute/path/to/'+fltData.company+fltData.flightNum+".jpg","JPEG")
        fltData.squack=squa
        fltData.stripImage=(MEDIA_ROOT+r"\DEPstrip{}".format(fltData.company+fltData.flightNum+"-"+dateOfflight+".jpg"))
        fltData.save()
        imagecreationstatus=True

        # baseimage.show()
    except:
        imagecreationstatus=False
    return imagecreationstatus


# printer  process
def printStripFunction(id):


    flt=flight.objects.get(id=id)
    try:
        # https://stackoverflow.com/questions/53765699/python-win32print-job-status
        # printing
        # p=win32print.OpenPrinter('OneNote')
        # i set the printer to landscape
        p=win32print.GetDefaultPrinter()
        print("the printer is: "+p)
        image_name=str(flt.stripImage)
        print(image_name)

        hdc=win32ui.CreateDC()
        hdc.CreatePrinterDC(p)
        printer_size=hdc.GetDeviceCaps(110),hdc.GetDeviceCaps(111)
        print(printer_size)

        bmp=Image.open(image_name)
        if bmp.size[0]>bmp.size[1]:
            print("horizental strip width > hieght")
        else:
            print("vertical strip width < hieght")
            bmp=bmp.rotate(90)

        print("size 0 is: "+str(bmp.size[0]))
        print("size 1 is: "+str(bmp.size[1]))

        hdc.StartDoc(image_name)
        hdc.StartPage()

        dib=ImageWin.Dib(bmp)
        dib.draw(hdc.GetHandleOutput(),(0,0,printer_size[1],printer_size[0]-6000))


        hdc.EndPage()
        hdc.EndDoc()
        hdc.DeleteDC()
        # save printed and squack
        flt.printed=True
        flt.save()
        printingStatus=True
    except:
        printingStatus=False
    return printingStatus
