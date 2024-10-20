from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import IntegrityError


def index(request):
    return render (request,'index.html')


def aboutus(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

# this is a function which will register user
def signup(request):
    if request.method == 'POST':
        # taking data form request
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # creating and saving a user instance
        try :
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()

            # logging in the user
            user = authenticate(request, username = username , password = password)
            if user is not None:
                login(request,user)

            # redirecting with message
                messages.add_message(request, messages.SUCCESS, "User Created Sucessfully!")
                return redirect('/')
            else:
                messages.add_message(request, messages.WARNING, "Some Error Occured!") 
                return redirect('signup')

        except IntegrityError:
            messages.add_message(request, messages.WARNING,'Credentials Already Taken!')
            return redirect('signup')
    else:
        return render(request,'signup.html')

    

# this is a function which will signin user
def signin(request):
    if request.method == 'POST':
        # taking data from request
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('landing_page')
        else:
            messages.add_message(request, messages.ERROR, "Invalid Credentials!")
            return redirect('signin')
    else:
        return render(request,'signin.html')
    

