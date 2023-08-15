
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User ,auth
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Profile

#decorator for user to enter home page after authentication

#home page
@login_required(login_url='login')
def IndexPage(request):
 user_object=User.objects.get(username=request.user.username)
 user_profile=Profile.objects.get(user=user_object)
 return render (request,'index.html',{'user_profile': user_profile}) 

#signup

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        
        
         
        if pass1==pass2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('signup')
            # messages.info(request,'password not match!!')
            elif User.objects.filter(username=uname).exists():
                messages.info(request,'Username Taken')
                return redirect('signup')
            else:
             my_user=User.objects.create_user(uname,email,pass1)
             my_user.save()
             #redirecting into setting page
             user_login=auth.authenticate(username=uname,password=pass1)
             auth.login(request,user_login)
             
             #create profile for new user
             user_model = User.objects.get(username=uname)
             new_profile = Profile.objects.create(user=user_model,id_user=user_model.id)
             new_profile.save()
             return redirect('settings')
        else:
            messages.info(request,'Password not matched')
            return redirect('signup')
    else:    
      return render (request,'signup.html')

    

#login
def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
       
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
         
        else:
            messages.info(request,'Credentials Invalid')
            return redirect('login')
    else:
      return render(request,'login.html')



#logout button
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


#settings
@login_required(login_url='login')
def settings(request):
 user_profile = Profile.objects.get(user=request.user)
 if request.method == 'POST':
    if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
    if request.FILES.get('image') != None:
          image = request.FILES.get('image')
          bio = request.POST['bio']
          location = request.POST['location']

          user_profile.profileimg = image
          user_profile.bio = bio
          user_profile.location = location
          user_profile.save()
    return redirect('settings')
 return render(request, 'setting.html', {'user_profile': user_profile})


#uploading_post
def upload(request):
    return HttpResponse('<h1> Upload View</h1>')