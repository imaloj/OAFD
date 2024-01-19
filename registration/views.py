from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User

def HomePage(request):
    return render(request,'home.html')
def SignupPage(request):
   #return HttpResponse("Username already exists. Please choose a different one.")
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        if pass1!=pass2:
            return HttpResponse("Your passwords doesn't match")
        else :
            my_user=User.objects.create_user(uname,email,pass1)
        my_user.save()
        return redirect('login')
        
    return render(request,'signup.html')
def LoginPage(request):
    return render(request,'login.html')
 