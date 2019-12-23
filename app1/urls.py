from django.conf.urls import url
from app1 import views
from django.urls import path

app_name='app1'


urlpatterns=[
          path('login/', views.login,name='default_login'),
          path('login/<msg>/', views.login,name='login'),
          path('mail/', views.mail,name='mail'),
          url(r'^register/', views.Register,name='register'),
          path('test/<message>/',views.test,name='test'),
          path('flightinfo/',views.flightinfo,name='flightinfo'),
          path('initialinfo/',views.main,name='initialinfo'),
          path('flightlist/',views.flightlist,name='flightlist'),
          path('uploadexcel/',views.uploadexcel,name='uploadexcel'),
          # path('deleteflight/', views.deleteflight, name='deleteflight'),
          path('flightUpdate/<int:id>/',views.flightUpdate,name='flightUpdate'),
          path('printStrip/',views.printStrip,name='printStrip'),
          path('getflightlist/',views.getflightlist,name='getflightlist'),









]
