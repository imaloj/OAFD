# from django.contrib import admin

# admin.site.register([Student,Teacher,Attendance])
from django.contrib import admin
from .models import ProductKey, AdminDetail, Teacher
# Register your models here.


admin.site.register(ProductKey)
admin.site.register(AdminDetail)
admin.site.register(Teacher)
