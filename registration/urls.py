from django.urls import path
from registration import views

urlpatterns = [
    # path('',views.SignupPage,name='signup'),
    # path('login/',views.LoginPage,name='login'),
    # path('home/',views.HomePage,name='home'),path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('signup/teacher_registration/', views.teacher_registration, name='teacher_registration'),
    path('', views.login, name='login'),
     path('home/', views.home, name='home'),
]