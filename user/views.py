from django.shortcuts import render, redirect, get_object_or_404
from .models import user

#Create New User
def create_user(request):
     if request.method == 'POST':
          username = request.POST['username']
          email = request.POST['email']
          user.objects.create(username=username , email=email)
          return redirect('all_users')
     return render(request, 'user/create.html')

# Read All Users
def all_users(request):
     users = user.objects.all()
     return render(request, 'user/list.html', {'users':users})

# Read one User
def user_detail(request, pk):
    user_obj = get_object_or_404(user, pk=pk)

    return render(request, 'user/detail.html', {'user': user_obj})

# Update user
def update_user(request, pk):
     user_obj = get_object_or_404(user , pk=pk)
     if request.method == 'POST':
          user_obj.username = request.POST['username']
          user_obj.email = request.POST['email']
          user_obj.save()
          return redirect('user_detail',pk=user_obj.pk)
     return render(request, 'user/update.html', {'user':user_obj})

# Delete User
def delete_user(request, pk):
     user_obj = get_object_or_404(user , pk=pk)
     if request.method == 'POST':
          user_obj.delete()
          return redirect('all_users')
     return render(request, 'user/delete.html', {'user':user_obj})