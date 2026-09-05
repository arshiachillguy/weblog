from django.urls import path 
from . import views

urlpatterns = [ 
     path('', views.all_users, name='all_users'),
     path('create/',views.create_user, name='create_user'),
     path('<int:pk>/', views.user_detail, name='user_detail'),
     path('<int:pk>/update/',views.update_user,name='update_user'),
     path('<int:pk>/delete/',views.delete_user,name='delete_user')
]