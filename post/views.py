from django.shortcuts import render, redirect, get_object_or_404
from .models import post
from django.contrib.auth.models import User


# Create New post
def create_post(request):
     if request.method == 'POST':
          title = request.POST['title']
          content = request.POST['content']
          author_id = request.POST['author']
          post.objects.create(title=title,content=content,author_id=author_id)
          return redirect('all_posts')

     users = User.objects.all()

     return render(request, 'post/create.html',{'users':users})

# Read All posts
def all_posts(request):
     posts = post.objects.all()
     return render(request, 'post/list.html', {'posts':posts})

# Real post detil
def post_details(request, pk):
     post_obj = get_object_or_404(post , pk=pk)
     return render(request, 'post/detail.html',{'post':post_obj})

# Update Post
def update_post(request, pk):
     post_obj = get_object_or_404(post, pk=pk)
     if request.method == 'POST':
          post_obj.title = request.POST['title']
          post_obj.content = request.POST['content']
           
          post_obj.save()
          return redirect('post_details',pk=post_obj.pk)

     return render(request, 'post/update.html',{'post':post_obj})

#Delete post
def delete_post(request, pk):
     post_obj = get_object_or_404(post,pk=pk)

     if request.method == 'POST':
          post_obj.delete()

          return redirect('all_posts')
     return render(request,'post/delete.html',{'post':post_obj})