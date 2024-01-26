from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image as PILImage #for opening and manipulating image
import numpy as np
import cv2
import io
import pymysql
import base64
from io import BytesIO

# Connect to the MySQL database
# connection = pymysql.connect(host='localhost', user='username', password='password', db='database_name')
# cursor = connection.cursor()

# # Create a table to store the images
# query = """CREATE TABLE IF NOT EXISTS images (id INT AUTO_INCREMENT PRIMARY KEY, image LONGBLOB)"""
# cursor.execute(query)

face_cascade = cv2.CascadeClassifier(self.Dir + '/haarcascade_frontalface_default.xml' )
video_cap=cv2.VideoCapture(1)
if not video_cap.isOpened():
    print("Error:Could not open Camera.")

def Captureframes(frame):
    while True :
        ret ,video_data=video_cap.read()
        if video_data is None:
            print("Error:Empty Frames.")
            return
        gray=cv2.cvtColor(video_data,cv2.COLOR_BGR2GRAY)
        faces= face_cascade.detectMultiScale(
        gray, 
        scaleFactor=1.1,
        minNeighbours=5,
        minSize=(30,30),
        flags=cv2.CASCADE_SCALE_IMAGE
        )
        for(x,y,w,h) in faces:
            cv2.rectangle(video_data,(x,y), (x+w,y+h),(0,255,0),2)
            cv2.imshow("video_live",video_data)
            if cv2.waitkey(10)&OxFF==ord("a"):
                break
            # Save the frame to the database
            image = Image.fromarray(video_data)
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            query = """INSERT INTO images (image) VALUES (%s)"""
            cursor.execute(query, (img_str,))
    video_cap.release()
    cv2.destroyAllWindows()

def SignupPage(request):
    return render(request,'signup.html')

def LoginPage(request):
    return render(request,'login.html')

def HomePage(request):
    return render(request,'home.html')

@csrf_exempt
def UploadImage(request):

    if request.method=='POST':
        image=request.FILES['image']
        pil_image=Image.open(image)#for reading and converting image to image object
        video_data= np.array(pil_image)
        result=Captureframes(video_data)
        image_io=io.BytesIO()
        cv2.imwrite(image_io,result)
        image_io.seek(0)
        return HttpResponse(image_io.getvalue(),content_type="image/png")
    else:
        return render(request , 'upload.html')
