from django.urls import path
from . import views

urlpatterns = [
    path('login', views.UserViewSet.as_view({'post': 'login'}), name='login'),
    path('register', views.UserViewSet.as_view(
        {'post': 'register'}), name='register'),
    path('user/images', views.UserViewSet.as_view({'get': 'fetchImages',
         'post': 'saveImages'}), name='user-images'),
    path('images', views.UserViewSet.as_view({'get': 'fetchImages',
         'post': 'saveImages'}), name='user-images'),
]
