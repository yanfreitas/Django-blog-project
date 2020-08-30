from django.urls import path
from blog import views
from blog.views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentDeleteView,
    UserPostListView,
    LikeView,
)


urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-post'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('post/comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('post/<int:pk>/like/', LikeView, name='like-post'),
]