from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "username taken")
                return redirect('credential:register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email taken")

                return redirect('credential:register')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,email=email, password=password)
                user.save()
                return redirect('credential:login')
        else:
            messages.info(request, "passwords not matching")
            return redirect('credential:register')

        return redirect('/')
    return render(request, 'register.html')


def login(request):
    print("enter")
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            print("login")
            return redirect('/')
        else:
            messages.info(request,"Invalid credentials")
            print("Invalid credentials")
            return redirect('credential:login')
    return render(request,'login.html')
def logout(request):
    auth.logout(request)
    return redirect('/')
# Create your views here.
