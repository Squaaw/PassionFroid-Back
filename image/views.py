from django.shortcuts import render
from django.contrib.auth import authenticate
import json
from django.http import QueryDict
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import connection
from django.db.models import Max
from rest_framework import status, viewsets
from .serializers import ImageSerializer
from tags.serializers import TagsSerializer
from .models import Image
from users.services import (describe_image_from_base64, get_image_vector_from_base64, get_image_vector_from_url, get_text_vector, get_cosine_similarity)
from image.services import get_images_from_db
from urllib.parse import unquote
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SomeCustomException(BaseException):
    pass

class ImageViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def max_id(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLE STATUS LIKE 'image_image'")
            row = cursor.fetchone()
            auto_increment_value = row[10]
        return Response({'max_id': auto_increment_value})

    def get(self, request, *args, **kwargs):
        userAuthentication = authenticate(username="admin" , password="Imie-paris2023")
        imagesWithTags = []
        if(userAuthentication is not None):
            images = Image.objects.all().raw("SELECT image.*, group_concat(tag.name separator ', ') AS tags FROM image_image AS image INNER JOIN tags_tags AS tag ON image.id = tag.image_id GROUP BY image.id")
            print("images")
            for image in images:
                imageObject = {
                        "id": image.id,
                        "name": image.name,
                        "base64": image.base64,
                        "description": image.description,
                        "width": image.width,
                        "height": image.height,
                        "created_at": image.created_at,
                        "updated_at": image.updated_at,
                        "tags": image.tags,
                    }
                imagesWithTags.append(imageObject)
            return Response(imagesWithTags, status=status.HTTP_200_OK)
        else:
            return Response({'msg': f'Vous n\'avez pas accès à cette ressource'}, status=status.HTTP_401_UNAUTHORIZED)

    
    @action(detail=False, methods=['post'])
    def getImagesSimilarity(self, request, *args, **kwargs):
        try:
            print("request.data.get")
            search_text = request.data.get("search")
            if not search_text:
                raise ValidationError("Search text is missing in the request.")
            
            getTextVector = get_text_vector(request.data.get("search"))

            imagesFromDb = Image.objects.all() 

            imagesSearch = []

            for image in imagesFromDb:
                getImageVector = image.vector
                print("getImageVector")
                print(getImageVector)
                if not getImageVector:
                    print("not image vector")
                # Handle the case where an image vector is missing or invalid.
                    continue

                getCosinusSimilarity = get_cosine_similarity(getImageVector, getTextVector)
                percentageSimilarity = getCosinusSimilarity * 100

                print("percentageSimilarity")
                print(percentageSimilarity)
                print(image.name)
                if(percentageSimilarity >= 25):
                    imageObject = {
                        "id": image.id,
                        "name": image.name,
                        "base64": image.base64,
                        "description": image.description,
                        "width": image.width,
                        "height": image.height,
                        "created_at": image.created_at,
                        "updated_at": image.updated_at,
                        "similarity": percentageSimilarity,
                    }
                    print("imageObject")
                    print(imageObject)
                    imagesSearch.append(imageObject)

            return Response(imagesSearch, status=status.HTTP_200_OK)

        except SomeCustomException as error:
           return Response({'msg': f'{error}'}, status=status.HTTP_400_BAD_REQUEST)
        

    def post(self, request):
        userAuthentication = authenticate(username="admin" , password="Imie-paris2023")
       
        if(userAuthentication is not None):
            try:
                user = User.objects.get(username="admin")
                base64 = request.data.get("base64")
                print("user")
                print(user)
                cognitiveObjet = describe_image_from_base64(base64)
                imageVector = get_image_vector_from_base64(base64)
         
                emptyTags = "No tags available"
                emptyDescription = "No description available"
       
    
                description = emptyDescription if cognitiveObjet.captions is None else cognitiveObjet.captions[0].text

                name = request.data.get('name')
                
                width = request.data.get('width')
                height = request.data.get('height')
               
                tagsFromB64 = cognitiveObjet.tags
             
                # Authentification de l'utilisateur.
                image = {
                        'name': name,
                        'description': description,
                        'base64': base64,
                        'width' : width,
                        'height': height,
                        'vector': imageVector
                    }
           
                serializer = ImageSerializer(data=image)

                if serializer.is_valid(raise_exception=True):
                    serializer.save(user=user)
                    print("image")
                    imageObj = Image.objects.get(id=serializer.data['id'])
                    for tagB in tagsFromB64:
                        
                        tag = {
                            'name': tagB
                        } 
                        tagSerializer = TagsSerializer(data=tag)
                        if tagSerializer.is_valid(raise_exception=True):
                            tagSerializer.save(image=imageObj)
                    
                return Response({'msg': "L'image a correctement été créee", 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
            except Exception as error:
                if status.HTTP_400_BAD_REQUEST:
                    return Response({'msg': f'Cette image existe déjà. veuillez en choisir une autre'}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response({'msg': f'Vous n\'avez pas les droits pour effectuer cette action'}, status=status.HTTP_400_BAD_REQUEST)
        
    
        

class ImageViewSetDetails(viewsets.ViewSet):
    """
    Retrieve, update or delete a snippet instance.
    """
    
    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ImageSerializer(snippet)
        return Response(serializer.data)

  
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ImageSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ImageSerializer(snippet, data=request.data)
        if serializer.is_valid():
            print(serializer.data)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)