from django.urls import path
from .import views
from .feeds import LatestReferencesFeed

app_name = 'reference'
urlpatterns = [
    path('', views.ReferenceListView.as_view(), name='reference_list'),
    # path('reference/<int:pk>-<slug:slug>/', views.ReferenceDetailView.as_view(), name='reference_detail'),
    path('feed/', LatestReferencesFeed(), name='reference_feed'),
    path('reference/add/', views.ReferenceCreateView.as_view(), name='reference_create'),
    path('reference/<int:pk>-<slug:slug>/update/', views.ReferenceUpdateView.as_view(), name='reference_update'),
    path('reference/<int:pk>-<slug:slug>/delete/', views.ReferenceDeleteView.as_view(), name='reference_delete'),
]