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
        imageIdList = Tags.objects.filter(name__in=tags).values_list("image_id", flat=True).distinct()
        imageJoin = ",".join(str(imageId) for imageId in imageIdList)
        imageList = Image.objects.all().raw(f"SELECT DISTINCT image.*, group_concat(tag.name separator ',') AS tags FROM image_image AS image INNER JOIN tags_tags AS tag ON image.id = tag.image_id WHERE image.id IN ({imageJoin}) GROUP BY image.id")

        imagesSearch = []

        for image in imageList:
            
            imageObject = {
                "id": image.id,
                "name": image.name,
                "base64": image.base64,
                "description": image.description,
                "width": image.width,
                "height": image.height,
                "created_at": image.created_at,
                "updated_at": image.updated_at,
                "tags": image.tags.split(",")
            }
                
            imagesSearch.append(imageObject)
       
        return Response(imagesSearch, status=status.HTTP_200_OK)