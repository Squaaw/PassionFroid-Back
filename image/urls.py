from django.urls import path
from . import views

urlpatterns = [
    path('images', views.ImageViewSet.as_view({'post': 'post'}), name='post'),
    path('image-details', views.ImageViewSetDetails.as_view({'delete': 'delete'}), name='delete'),
   # path('image/custom-method', include('image.urls')),
    path('images/<int:pk>/', views.ImageViewSetDetails.as_view({'get': 'retrieve'}), name='image-detail'),
    path('images/<int:pk>/update', views.ImageViewSetDetails.as_view({'put': 'put'}), name='image-update'),
    path('images/<int:pk>/delete', views.ImageViewSetDetails.as_view({'delete': 'delete'}), name='image-delete'),
    path('images-tags/', views.ImageViewSet.as_view({'get': 'custom_method'}), name='list-categories'),
    path('images/max_id/', views.ImageViewSet.as_view({'get': 'max_id'}), name='image-max-id'),
    path('images/search/', views.ImageViewSet.as_view({'post': 'getImagesSimilarity'}), name='image-search'),
]