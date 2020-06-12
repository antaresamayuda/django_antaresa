from django.urls import path
from .import views
from .feeds import LatestPostsFeed

app_name = 'reference'
urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>-<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('post/add/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>-<slug:slug>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>-<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]