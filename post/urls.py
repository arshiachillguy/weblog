from django.urls import path

from . import views

urlpatterns = [
     #HTML pages 
     path('', views.all_posts, name='all_posts'),
     path('create/',views.create_post,name='create_post'),
     path('<int:pk>/',views.post_details , name='post_details'),
     path('<int:pk>/update/',views.update_post,name='update_post'),
     path('<int:pk>/delete/',views.delete_post,name='delete_post'),
     
     # API 
     path('api/posts/',views.post_list_create_api , name='post_list_create_api'),
     path('api/posts/<int:pk>/', views.post_detail_api, name='post_detail_api'),
     
]