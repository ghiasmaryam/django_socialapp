
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User ,auth
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Profile

#decorator for user to enter home page after authentication
@login_required(login_url='login')

#home page
def IndexPage(request):
 return render (request,'index.html') 

#signup

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        
        
         
        if pass1!=pass2:
            messages.info(request,'password not match!!')
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            user_model = User.objects.get(username=uname)
            new_profile = Profile.objects.create(user=user_model,id_user=user_model.id)
            new_profile.save()
            return redirect('login')
        
    return render (request,'signup.html')

    

#login
def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        print(username,pass1)
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('index')
         
        else:
            messages.info(request,'Credentials Invalid')
    
    return render(request,'login.html')



#logout button

def LogoutPage(request):
   auth.logout(request)
   return redirect('login')
