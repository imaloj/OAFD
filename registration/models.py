# from django.db import models
# from django.contrib.auth.models import User
# gender_list=(('Male','Male'),('Female','Female'))
# class Teacher(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE),
#     gender =models.CharField(max_length=10,choices=gender_list),
#     room=models.CharField(max_length=5),
#     is_delete =models.BooleanField(default=False)
# class Student(models.Model):
#  STU_ID=models.CharField(max_length=20,unique=True,null=False, primary_key=True),
#  STU_NAME=models.CharField(max_length=20,null=False),
#  STU_FACULTY=models.CharField( max_length=50,null=False)
#  STU_ADD=models.CharField(max_length=50,null=False),
#  STU_PHONE=models.CharField(max_length=10,null=False),
#  STU_EMAIL=models.CharField(max_length=50,null=False),
#  Photo_taken= models.BooleanField 
#  def __str__(self):
#     return self.name 

# class Teacher(models.Model):
#     STU_ID=models.CharField(max_length=20,unique=True,null=False, primary_key=True),    
from django.db import models
import os


def get_image_path(instance, filename):
    return os.path.join('profile_images/', str(instance.teacher_id), filename)


# Create your models here.
class ProductKey(models.Model):
    product_key = models.CharField(max_length=100, primary_key=True)

    class Meta:
        db_table = 'Product_Key'


class AdminDetail(models.Model):
    product_key = models.ForeignKey(ProductKey, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    organisation = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    

    class Meta:
        db_table = 'Admin_Detail'


class Teacher(models.Model):
    product_key = models.CharField(max_length=100,default='1')
    teacher_name = models.CharField(max_length=100,null=False,default='Ripper')
    teacher_id = models.CharField(max_length=100, primary_key=True, default='IT-00000',unique=True)
    number = models.IntegerField(null=False,blank=False,unique=True,default='9800000000',help_text='Enter Your Number')
    department = models.CharField(max_length=100, default='BSc.CSIT')
    profile_photo = models.ImageField(upload_to=get_image_path,null=False,default='Nophoto')
    def __str__(self):
        return self.name
    

    class Meta:
        db_table = 'teacher_details'

