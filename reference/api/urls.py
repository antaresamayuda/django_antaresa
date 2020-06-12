from django.urls import path
from . import views

app_name='reference'
urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='api_post_list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='api_post_detail'),
]