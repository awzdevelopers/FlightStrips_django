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





]
