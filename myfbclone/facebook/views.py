from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

#decorator for user to enter home page after authentication
@login_required(login_url='login')
#home page
def HomePage(request):
 return render (request,'home.html') 

#signup

def SignupPage(request):
    if request.method=='POST':
       uname=request.POST.get('username')  
       email=request.POST.get('email')
       pass1=request.POST.get('password1') 
       pass2=request.POST.get('password2')
    
       if pass1!=pass2:
        return HttpResponse("PASSWORD NOT MATCHED")
       else:
        my_user=User.objects.create_user(uname,email,pass1)
        my_user.save()
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
            return redirect('home')
        else:
            return HttpResponse ("Incorrect username or password")
    
    return render(request,'login.html')



#logout button

def LogoutPage(request):
    logout(request)
    return redirect('login')
