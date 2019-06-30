from django.contrib import admin
from django.urls import path
from .views import PostListView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('user/<str:username>/', views.UserPostListView.as_view(), name='user-posts'),
    path('user/<int:pk>/', views.UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/',views.PostDetailView,name='detail'),
    path('post/new/',views.PostCreateView.as_view(),name='post-create'),
    path('post/<int:pk>/update/',views.PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete/',views.PostDeleteView.as_view(),name='post-delete'),
    path('about/', views.about, name='about'),
    path('like/', views.like_post, name='like_post'),
]
