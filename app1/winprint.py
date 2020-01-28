import os,sys
import win32print


p=win32print.OpenPrinter('OneNote')
job=win32print.StartDocPrinter(p,1,("test priniting message",None,"RAW"))
win32print.StartPagePrinter(p)
win32print.WritePrinter(p,1235468)
win32print.EndPagePrinter(p)
