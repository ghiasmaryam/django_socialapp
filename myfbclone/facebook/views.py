
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User ,auth
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Profile,Post,LikePost,FollowersCount

#decorator for user to enter home page after authentication

#home page
@login_required(login_url='login')
def IndexPage(request):
 user_object = User.objects.get(username=request.user.username)
 user_profile = Profile.objects.get(user=user_object)


  #to show uploaded post on index
 posts=Post.objects.all()
 return render(request, 'index.html', {'user_profile': user_profile,'posts':posts})

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
             return redirect('login')
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
    if request.method=='POST':
        user=request.user.username
        image=request.FILES.get('image_upload')
        caption=request.POST['caption']
        
        new_post=Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        
        return redirect('/')
    else:
        return redirect('/')   
    

#likes_on_post  
@login_required(login_url='login')
def like_post(request):  
    username=request.user.username
    post_id=request.GET.get('post_id')
    
    post=Post.objects.get(id=post_id)
    
    like_filter =LikePost.objects.filter(post_id=post_id,username=username).first()
    if like_filter==None:
        new_like =LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_of_likes=post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes-1
        post.save()
        return redirect('/')
    
    #user_profile_screen



#user_profile_screen
@login_required(login_url='login')
def profile(request, pk):
    user_object= User.objects.get(username=pk)
    user_profile=Profile.objects.get(user=user_object)
    user_posts=Post.objects.filter(user=pk)
    user_post_length=len(user_posts)
        
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts':user_posts,
        'user_post_length':user_post_length,
    }
    return render(request,'profile,html')


#follow_user
@login_required(login_url='login')
def follow(request):
    if request.method =='POST':
       follower = request.POST['follower']
       user=request.POST['user'] 
       
       if FollowersCount.objects.filter(follower=follower,user=user).first():
           delete_follower=FollowersCount.objects.get(follower=follower,user=user)
           delete_follower.delete()
           return redirect('/profile'+user)
       else:
          new_follower=FollowersCount.objects.create(follower=follower,user=user)
          new_follower.save()
    else:
     return redirect('/')   
    