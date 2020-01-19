from django.contrib import admin
from app1.models import user,flight,companyList,typeList,DaysOfweek,loggingTable

# Register your models here.
admin.site.register(user)
admin.site.register(flight)
admin.site.register(companyList)
admin.site.register(typeList)
admin.site.register(DaysOfweek)
admin.site.register(loggingTable)
