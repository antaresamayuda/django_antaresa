from django.urls import path
from . import views

app_name='reference'
urlpatterns = [
    path('list/', views.ReferenceListView.as_view(), name='api_reference_list'),
    path('list/<int:pk>/', views.ReferenceDetailView.as_view(), name='api_reference_detail'),
]