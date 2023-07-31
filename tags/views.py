from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from rest_framework import viewsets, status
from .serializers import TagsSerializer
from image.serializers import ImageSerializer
from rest_framework.response import Response
from .models import Tags, Image
# Create your views here.
class TagsViewSet(viewsets.ViewSet):

    def get(self, request, *args, **kwargs):
        print("test get")
        userAuthentication = authenticate(username="admin" , password="Imie-paris2023")
       
        if(userAuthentication is None):
            return Response({'msg': f'Vous n\'avez pas accès à cette ressource'}, status=status.HTTP_401_UNAUTHORIZED)
     
        distinctTags = Tags.objects.values_list('name', flat=True).distinct()
        return Response(distinctTags, status=status.HTTP_200_OK)
        

    
    def post(self, request, *args, **kwargs):
        userAuthentication = authenticate(username="admin" , password="Imie-paris2023")
        if(userAuthentication is None):
            return Response({'msg': f'Vous n\'avez pas accès à cette ressource'}, status=status.HTTP_401_UNAUTHORIZED)
           
        tags = request.data.get("tags")

        imageId = Tags.objects.filter(name__in=tags).values_list("image_id", flat=True).distinct()
        imageList = Image.objects.filter(id__in=imageId)

        serializerByImage = ImageSerializer(imageList, many=True)
        # print("serializerByImage.data")
        # print(serializerByImage.data)
        return Response(serializerByImage.data, status=status.HTTP_200_OK)