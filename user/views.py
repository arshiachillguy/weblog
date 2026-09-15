from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .forms import RegisterForm , LoginForm , CreateUserForm , UpdateUserForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer ,ProfileSerializer
from rest_framework.permissions import IsAuthenticated

#----AUTHENTICATION
def register_page(request):
     form = RegisterForm(request.POST or None)
     if form.is_valid():
          user = form.save()
          login(request, user)

          return redirect('home')
          
     return render(request,'register.html' , {'form':form})

def login_page(request):
     form = LoginForm(request , data=request.POST or None)
     if form.is_valid():
          user =form.get_user()
          login(request , user)
          return redirect('home')
     return render(request, 'login.html', {'form':form})

def logout_view(request):
     logout(request)
     return redirect("login_page")



def home(request):
    return render(request, 'home.html')

#----CRUD
#Create New User
# admin can make user 
@staff_member_required
def create_user(request):
     form = CreateUserForm(request.POST or None)
     if form.is_valid():
          form.save()
          return redirect('all_users')

     return render(request, 'user/create.html',{'form':form})

# Read All Users
# admin can read all data about users
@staff_member_required
def all_users(request):
     users = User.objects.all()
     return render(request, 'user/list.html', {'users':users})

# Read one User
def user_detail(request, pk):
    user_obj = get_object_or_404(User, pk=pk)

    return render(request, 'user/detail.html', {'user': user_obj})

# Update user
@login_required
def update_user(request, pk):
     user_obj = get_object_or_404(User , pk=pk)
     # user should update itself not any one it wants 
     if user_obj != request.user:
          return redirect('home')

     form = UpdateUserForm(request.POST or None , instance=user_obj)
     if form.is_valid():
          form.save()
          return redirect('user_detail',pk=user_obj.pk)
     return render(request, 'user/update.html', {'form':form})

# Delete User
@login_required
def delete_user(request, pk):
     user_obj = get_object_or_404(User , pk=pk)

     # user should delete itself not any one      
     if user_obj != request.user:
          return redirect('all_posts')


     if request.method == 'POST':
          user_obj.delete()
          logout(request)
          return redirect("login_page")
     return render(request, 'user/delete.html', {'user':user_obj})

@login_required
def changePassword(request):
     form = PasswordChangeForm(request.user ,request.POST or None)
     if form.is_valid():
          user = form.save()
          #prevent to logout user automaticly 
          update_session_auth_hash(request, user)
          return redirect('home')
     return render(request , 'user/change_password.html' , {'form':form})     



@api_view(['GET', 'POST'])
def user_list_create_api(request):
          
     if request.method == "GET":
          users = User.objects.all()

          serializer = UserSerializer(users, many=True)
          
          return Response(serializer.data)

     elif request.method == "POST":
          serializer = UserSerializer(data=request.data)

          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data , status=201)

     return Response(serializer.errors , status=400)

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.contrib.auth.models import User

from .serializers import UserSerializer


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def user_detail_api(request, pk):

    user_obj = get_object_or_404(User, pk=pk)

    # Read user
    if request.method == 'GET':

        serializer = UserSerializer(user_obj)

        return Response(serializer.data)

    # Update full user
    elif request.method == 'PUT':

        if user_obj != request.user:
            return Response(
                {"detail": "You do not have permission to edit this user."},
                status=403
            )

        serializer = UserSerializer(user_obj,data=request.data)

        if serializer.is_valid():

          erializer.save()

          return Response(serializer.data)

        return Response(serializer.errors, status=400)

    # Update partial user
    elif request.method == 'PATCH':

        if user_obj != request.user:
            return Response(
                {"detail": "You do not have permission to edit this user."},
                status=403)

        serializer = UserSerializer(user_obj,data=request.data,partial=True)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    # Delete user
    elif request.method == 'DELETE':

        if user_obj != request.user:
            return Response(
                {"detail": "You do not have permission to delete this user."},
                status=403)

        user_obj.delete()

        return Response({"message": "User deleted successfully"})

#gathering data for profile api 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_api(request):

     user_obj = request.user
     
     serializer = ProfileSerializer(user_obj)
     
     return Response(serializer.data)

