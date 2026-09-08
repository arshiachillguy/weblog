from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
#----AUTHENTICATION
def login_page(request):
     if request.method == "POST":
          username = request.POST.get('username')
          password = request.POST.get('password')

          if not User.objects.filter(username=username).exists():
               messages.error(request, 'Invalid Username')
               return redirect('/user/login/')

          user = authenticate(username=username, password=password)

          if user is None:
               messages.error(request,'Invalid Password')
               return redirect('/user/login/')
          else:
               login(request,user)
               return render(request, 'home.html')
     return render(request, 'login.html')

def logout_view(request):
     logout(request)
     return redirect("login_page")


def register_page(request):
     if request.method == 'POST':
          username = request.POST.get('username')
          password = request.POST.get('password')
          email = request.POST.get('email')

          user = User.objects.filter(username=username)

          if user.exists():
               messages.info(request,"Username already taken!")
               return render(request, "register.html")

          user = User.objects.create_user(
               username=username,
               password=password,
               email=email
          )
          user.save()
          login(request,user)
          messages.info(request,"Account created Successfully!")
          return render(request , 'home.html')
          
     return render(request,'register.html')


#----CRUD
#Create New User
# admin can make user 
@staff_member_required
def create_user(request):
     if request.method == 'POST':
          username = request.POST['username']
          email = request.POST['email']
          password = request.POST['password']
          
          if User.objects.filter(username=username).exists():
               messages.error(request, "username already exits")
               return redirect('create_user')
          
          User.objects.create_user(username=username , email=email , password=password)
          return redirect('all_users')
     return render(request, 'user/create.html')

# Read All Users
# admin can read all data about users
@staff_member_required
def all_users(request):
     users = User.objects.all()
     return render(request, 'user/list.html', {'users':users})

# Read one User
def user_detail(request, pk):
    User_obj = get_object_or_404(User, pk=pk)

    return render(request, 'user/detail.html', {'user': User_obj})

# Update user
@login_required
def update_user(request, pk):
     User_obj = get_object_or_404(User , pk=pk)
     # user should update itself not any one it wants 
     if User_obj != request.user:
          return redirect('home.html')

     if request.method == 'POST':
          User_obj.username = request.POST['username']
          User_obj.email = request.POST['email']
          User_obj.save()
          return redirect('user_detail',pk=User_obj.pk)
     return render(request, 'user/update.html', {'user':User_obj})

# Delete User
@login_required
def delete_user(request, pk):
     User_obj = get_object_or_404(User , pk=pk)

     # user should delete itself not any one      
     if User_obj != request.user:
          return redirect('all_posts')


     if request.method == 'POST':
          User_obj.delete()
          return redirect('all_users')
     return render(request, 'user/delete.html', {'user':User_obj})