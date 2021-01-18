from django.urls import path
from users import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('<str:username>/', views.useroverview, name='useroverview'),
    path('<str:username>/userfollowers/', views.userfollowers, name='userfollowers'),
    path('<str:username>/userfollowing/', views.userfollowing, name='userfollowing'),
    path('<str:username>/profileupdate/', views.profileupdate, name='profileupdate'),
    path('follow/user', views.follow, name='follow'),
]
