from django.urls import path
from . import views

urlpatterns = [
    path('tags/', views.TagsViewSet.as_view({'get': 'get'}), name='get'),
    path('images-by-tags/', views.TagsViewSet.as_view({'post': 'post'}), name='post'),
    path('tags-remove-by-name/', views.TagsViewSet.as_view({'post': 'removeTagsByName'}), name='tag-name'),
]