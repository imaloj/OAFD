# from django.shortcuts import render,HttpResponse,redirect
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate,login
# from django.shortcuts import render
# from django.http import HttpResponse

# def HomePage(request):
#     return render(request,'home.html')
# def SignupPage(request):
#    #return HttpResponse("Username already exists. Please choose a different one.")
#     if request.method=='POST':
#         uname=request.POST.get('username')
#         email=request.POST.get('email')
#         pass1=request.POST.get('password1')
#         pass2=request.POST.get('password2')
#         if pass1!=pass2:
#             return HttpResponse("Your passwords doesn't match")
#         else :
#             my_user=User.objects.create_user(uname,email,pass1)
#         my_user.save()
#         return redirect('login')
        
#     return render(request,'signup.html')
# def LoginPage(request):
#     if request.method=='POST':
#         username=request.POST.get('username')
#         pass1=request.POST.get('password')
#         user=authenticate(request,username=username,password=pass1)
#         if user is not None:
#             login(request,user)
#             return redirect('home')
#         else:
#             return HttpResponse("Username or Password is incorrect!!!")
#     return render(request,'login.html')
from django.shortcuts import render, redirect, HttpResponse
from registration.models import AdminDetail, Teacher, ProductKey
from django.contrib import messages
from django.conf import settings
from wsgiref.util import FileWrapper
import mimetypes
from django.utils.encoding import smart_str
from registration.FaceRecognition import *
import cv2
import pandas as pd
from datetime import datetime


# Create your views here.
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == "POST":
        product_key = request.POST['product_key']
        name = request.POST['admin_name']
        number = request.POST['number']
        department = request.POST['department']
        username = request.POST['username']
        password = request.POST['pass1']
        password_repeat = request.POST['pass2']

        # Preparing check for product key
        product_key_check = ProductKey.objects.all()
        key_data = [key.product_key for key in product_key_check]

        # Preparing check for username
        username_check = AdminDetail.objects.all()
        username_data = [uname.username for uname in username_check]

        # Checking for duplicate username, false product key and password match
        if product_key not in key_data or username in username_data or password != password_repeat:
            if product_key not in key_data:
                messages.info(request, 'Wrong Product Key')
                return redirect('signup')
            el
            if username in username_data:
                messages.info(request, 'Username already taken')
                return redirect('signup')
            else:
                messages.info(request, 'Passwords do not match')
                return redirect('signup')
        else:
            obj = AdminDetail(None, product_key, name, number, department, username, password)
            obj.save()
            return redirect('teacher_registration')
    else:
        return render(request, 'signup.html')


def teacher_registration(request):
    if request.method == 'POST':
        product_key = request.POST['product_key']
        teacher_id = request.POST['teacher_id']
        teacher_name = request.POST['teacher_name']
        number = request.POST['number']
        department = request.POST['department']
        profile_photo = request.FILES['profile_photo']

        obj = teacher(product_key=product_key, teacher_name=teacher_name, teacher_id=teacher_id, number=number,
                       department=department, profile_photo=profile_photo)
        obj.save()
        return redirect('teacher_registration')
    else:
        return render(request, 'teacher_registration.html')


def login(request):
    if request.method == "POST":
        tecid = request.POST['tecid']

        obj = teacher.objects.filter(teacher_id=tecid)
        for data in obj:
            # Checking username and password
            if data.teacher_id == tecid:
                # Capturing image for recognition
                cap = cv2.VideoCapture(0)
                count = 0
                while True:
                    ret, test_img = cap.read()
                    if not ret:
                        continue
                    cv2.imwrite("media/frame.jpg", test_img)  # save frame as JPG file
                    count += 1
                    resized_img = cv2.resize(test_img, (1000, 700))
                    cv2.imshow('face detection Tutorial ', resized_img)
                    break
                # When everything done, release the capture
                cap.release()
                cv2.destroyAllWindows()

                # Detecting face
                # This module takes images  stored in diskand performs face recognition
                test_img = cv2.imread('media/frame.jpg')  # test_img path
                faces_detected, gray_img = faceDetection(test_img)
                print("faces_detected:", faces_detected)

                # Comment belows lines when running this program second time.Since it saves training.yml file in directory
                faces, faceID = labels_for_training_data('media/profile_images')
                face_recognizer = train_classifier(faces, faceID)
                face_recognizer.write('trainingData.yml')

                # Uncomment below line for subsequent runs
                # face_recognizer=cv2.face.LBPHFaceRecognizer_create()
                # face_recognizer.read('trainingData.yml')#use this to load training data for subsequent runs
                tec = teacher.objects.all()
                tec_id = [int(tec_id.teacher_id) for tec_id in tec]
                tec_name = [tec_name.teacher_name for tec_name in tec]
                name = dict(zip(tec_id, tec_name)) # creating dictionary containing names for each label
                print(name)

                for face in faces_detected:
                    (x, y, w, h) = face
                    roi_gray = gray_img[y:y + h, x:x + h]
                    label, confidence = face_recognizer.predict(roi_gray)  # predicting the label of given image
                    print("confidence:", confidence)
                    print("label:", label)

                    obj = teacher.objects.filter(teacher_id=label)
                    for names in obj:
                        ids = names.teacher_id
                        nams = names.teacher_name
                        depts = names.department
                        p_k = names.product_key

                        now = datetime.now()
                        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

                        data = [[ids, nams, depts, dt_string]]

                        df = pd.DataFrame(data, columns=['Id', 'Name', 'Department', 'Date'])

                        df.to_excel('media/' + p_k + '.xlsx')

                    draw_rect(test_img, face)
                    predicted_name = name[label]
                    if (confidence > 37):  # If confidence more than 37 then don't print predicted face text on screen
                        continue
                    put_text(test_img, predicted_name, x, y)

                resized_img = cv2.resize(test_img, (1000, 1000))
                cv2.waitKey(0)  # Waits indefinitely until a key is pressed
                cv2.destroyAllWindows()

                return redirect('/')
            else:
                return redirect('/')
        return redirect('/')
    else:
        return render(request, 'login.html')


def admin_login(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']

        obj = AdminDetail.objects.all()

        username_data = [uname.username for uname in obj]

        if username in username_data:
            obj = AdminDetail.objects.filter(username=username)
            for data in obj:
                if data.password == password:
                    key = data.product_key_id
                    file_name = key + '.xlsx'
                    file_path = settings.MEDIA_ROOT + '/' + file_name
                    file_wrapper = FileWrapper(open(file_path, 'rb'))
                    file_mimetype = mimetypes.guess_type(file_path)
                    response = HttpResponse(file_wrapper, content_type=file_mimetype)
                    response['X-Sendfile'] = file_path
                    response['Content-Length'] = os.stat(file_path).st_size
                    response['Content-Disposition'] = 'attachment; filename=%s/' % smart_str(file_name)
                    return response
                else:
                    messages.info(request, 'Incorrect Password')
                    return redirect('admin_login')
        else:
            messages.info(request, 'No Such User')
            return redirect('admin_login')

    else:
        return render(request, 'admin_login.html')

    
 