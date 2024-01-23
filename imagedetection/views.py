from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image as PILImage #for openind and manipulating image
import numpy as np
import cv2
import io
def SignupPage(request):
    return render(request,'signup.html')
def LoginPage(request):
    return render(request,'login.html')
def HomePage(request):
    return render(request,'home.html')


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcasde_frontalface_default.xml')
def detect_faces(image_array):
    gray=cv2.cvtColor(image_array,cv2.COLOR_BGR2GRAY)
    face= face_cascade.detectMultiScale(gray, scaleFactor=1.1 ,minNeighbours=5 , minSize=(30,30))
    for(x,y,w,h)in face:
        ret ,frame=cap.read()
        cv2.rectangle(image_array,(100,100), (200,200),(255,0,0),2)
        return image_array

@csrf_exempt
def UploadImage(request):
    if request.method=='POST':
        image=request.FILES['image']
        pil_image=Image.open(image)#for reading and converting image to image object
        image_array= np.array(pil_image)
        result=detect_faces(image_array)
        image_io=io.BytesIO()
        cv2.imwrite(image_io,result)
        image_io.seek(0)
        returnHttpResponse(image_io.getvalue(),content_type="image/png")
    else:
            return render(request , 'upload.html')

 

        
