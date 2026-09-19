from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .forms import InputForm
from .models import post
from .serializers import PostSerializer


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

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list_create_api(request):
    # if the req has GET method api shows the list of posts
    if request.method == 'GET':
        posts = post.objects.all()
        # for getting post author 
        author_filter = request.query_params.get('author')
        if author_filter:
            posts = posts.filter(author__username=author_filter)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    # if the req has POST method - api send the content to create new post 
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_detail_api(request, pk):

    post_obj = get_object_or_404(post, pk=pk)

    if request.method == 'GET':

          serializer = PostSerializer(post_obj)
          return Response(serializer.data)

    elif request.method == 'PUT':

          if post_obj.author != request.user:
               return Response(
                    {"detail": "You do not have permission to edit this post."},
                    status=403
               )

          serializer = PostSerializer( post_obj , data=request.data)

          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          
          return Response(serializer.errors, status=400)

    elif request.method == 'PATCH':

          if post_obj.author != request.user:
               return Response({"detail": "You do not have permission to edit this post."},status=403)

          serializer = PostSerializer(post_obj,data=request.data,partial=True)

          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)

          return Response(serializer.errors, status=400)


    elif request.method == 'DELETE':
        
          if post_obj.author != request.user:
               return Response(
               {"detail": "You do not have permission to delete this post."},
                    status=403
               )

          post_obj.delete()

          return Response({"message": "Post deleted successfully"})
