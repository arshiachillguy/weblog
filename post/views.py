from django.shortcuts import render, redirect, get_object_or_404
from .models import post
from django.contrib.auth.decorators import login_required
from .forms import InputForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create_api(request):

     serializer = PostSerializer(data=request.data)

     if serializer.is_valid():
          #jwt know who is this user !
          serializer.save(author=request.user)

          return Response(serializer.data)

@api_view(['GET'])
def post_list_api(request):

     posts = post.objects.all()
     serializer = PostSerializer(posts , many=True)

     return Response(serializer.data)

@api_view(['GET'])
def post_detail_api(request, pk):

    post_obj = get_object_or_404(post , pk=pk)

    serializer = PostSerializer(post_obj)

    return Response(serializer.data)
# use put for changing all data of post 
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def post_update_api(request, pk):

    post_obj = get_object_or_404(post, pk=pk)

    if post_obj.author != request.user:
        return Response(
         {"detail": "You do not have permission to edit this post."},
         status=403
     )

    serializer = PostSerializer( post_obj , data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
# use patch for chaning just fileds you want 
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def post_partial_update_api(request, pk):

    post_obj = get_object_or_404(post, pk=pk)

    if post_obj.author != request.user:
        return Response({"detail": "You do not have permission to edit this post."},status=403)

    serializer = PostSerializer(post_obj,data=request.data,partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def post_delete_api(request, pk):

    post_obj = get_object_or_404(post, pk=pk)

    if post_obj.author != request.user:
        return Response(
            {"detail": "You do not have permission to delete this post."},
            status=403
        )

    post_obj.delete()

    return Response({"message": "Post deleted successfully"})