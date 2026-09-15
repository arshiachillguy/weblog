from django.urls import path 
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)


urlpatterns = [     
     # Authentication
     path('login/', views.login_page, name='login_page'),
     path("logout/", views.logout_view, name="logout"),
     path('register/', views.register_page, name='register_page'),
     path('change-password',views.changePassword,name='changePassword'),

     # Users
     path('home/',views.home, name='home'),
     path('users/', views.all_users, name='all_users'),
     path('create/',views.create_user, name='create_user'),
     path('<int:pk>/', views.user_detail, name='user_detail'),
     path('<int:pk>/update/',views.update_user,name='update_user'),
     path('<int:pk>/delete/',views.delete_user,name='delete_user'),
     
     #JWT API 
     path('api/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
     path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),

     # main API
     
     path('api/users/',views.user_list_create_api, name='user_list_create_api'),
     path('api/users/<int:pk>/',views.user_detail_api,name='user_detail_api'),

     # profile API
     path('api/profile/',views.profile_api,name='profile_api'),

     #register API
     path('api/register/',views.register_api,name='register_api'),
]