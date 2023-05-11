from django.urls import path
from . import views

urlpatterns = [
    path('images/create', views.ImageViewSet.as_view({'post': 'saveImages'}), name='saveImages'),
    

]