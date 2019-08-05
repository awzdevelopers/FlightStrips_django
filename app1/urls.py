from django.conf.urls import url
from app1 import views


app_name='app1'


urlpatterns=[
          url(r'^login/', views.login,name='login'),
          url(r'^mail/', views.sendemail,name='mail'),
          url(r'^register/', views.Register,name='register'),
]
