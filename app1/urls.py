from django.conf.urls import url
from app1 import views
from django.urls import path
from app1.views import addFlightFromView


app_name='app1'


urlpatterns=[
          path('login/', views.login,name='default_login'),
          path('PrintPage/<int:id>/', views.PrintPage,name='PrintPage'),

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
          path('delFlight/<int:pk>', views.delFlight.as_view(), name='delFlight'),
          url(r'^addFlightFromView/',addFlightFromView.as_view()),
          url(r'^ajax/validate_company/$', views.validate_company, name='validate_company'),
          url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),

]
