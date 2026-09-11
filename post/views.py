from django.shortcuts import render, redirect, get_object_or_404
from .models import post
from django.contrib.auth.decorators import login_required
from .forms import InputForm

# Create New post
@login_required
def create_post(request):
     # if request.method == 'POST':
     form = InputForm(request.POST or None)
     if form.is_valid():
               post_obj = form.save(commit=False)
               post_obj.author = request.user
               post_obj.save()
               return redirect('all_posts')     

     return render(request, 'post/create.html' , {'form':form})

# Read All posts
def all_posts(request):
     posts = post.objects.all()
     return render(request, 'post/list.html', {'posts':posts})

# Real post detil
def post_details(request, pk):
     post_obj = get_object_or_404(post , pk=pk)
     return render(request, 'post/detail.html',{'post':post_obj})

# Update Post
@login_required
def update_post(request, pk):
     post_obj = get_object_or_404(post, pk=pk , author=request.user)
     

     form = InputForm(request.POST or None, instance=post_obj)     
     if form.is_valid():
         form.save()
         return redirect('all_posts')

     return render(request, 'post/update.html',{'form':form})

#Delete post
@login_required
def delete_post(request, pk):
     post_obj = get_object_or_404(post,pk=pk , author=request.user)

     if request.method == 'POST':
          post_obj.delete()
          return redirect('all_posts')

     return render(request,'post/delete.html',{'post':post_obj})