from django.db import models
class Student(models.Model):
 STU_ID=models.CharField(max_length=20,unique=True,null=False, primary_key=True),
 STU_NAME=models.CharField(max_length=20,null=False),
 STU_FACULTY=models.CharField( max_length=50,null=False)
 STU_ADD=models.CharField(max_length=50,null=False),
 STU_PHONE=models.CharField(max_length=10,null=False),
 STU_EMAIL=models.CharField(max_length=50,null=False),
 Photo_taken= models.BooleanField 
 def __str__(self):
    return self.name 

class Teacher(models.Model):
    STU_ID=models.CharField(max_length=20,unique=True,null=False, primary_key=True),    
