from django.shortcuts import render, redirect, get_object_or_404
from .models import post
from django.contrib.auth.decorators import login_required

# Create New post
@login_required
def create_post(request):
     if request.method == 'POST':
          title = request.POST['title']
          content = request.POST['content']

          post.objects.create(title=title,content=content,author=request.user)
          return redirect('all_posts')

     return render(request, 'post/create.html')

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
     if request.method == 'POST':
          post_obj.title = request.POST['title']
          post_obj.content = request.POST['content']
          post_obj.save()

          return redirect('post_details',pk=post_obj.pk)

     return render(request, 'post/update.html',{'post':post_obj})

#Delete post
@login_required
def delete_post(request, pk):
     post_obj = get_object_or_404(post,pk=pk , author=request.user)

     if request.method == 'POST':
          post_obj.delete()
          return redirect('all_posts')

     return render(request,'post/delete.html',{'post':post_obj})