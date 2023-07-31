from django.urls import path
from . import views

urlpatterns = [
    path('tags/', views.TagsViewSet.as_view({'get': 'get'}), name='get'),
    path('images-by-tags/', views.TagsViewSet.as_view({'post': 'post'}), name='post'),
]