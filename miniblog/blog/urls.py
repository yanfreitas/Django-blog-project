from django.urls import path
from blog import views


urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('<int:pk>', views.BlogDetailView.as_view(), name='blogpost-detail'),
    path('bloggers/', views.AuthorListView.as_view(), name='bloggers'),
    path('blogger/<int:id>', views.AuthorDetailView.as_view(), name='author-detail'),
]