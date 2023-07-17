from django.shortcuts import render
import json
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import connection
from django.db.models import Max
from rest_framework import status, viewsets
from .serializers import ImageSerializer
from .models import Image
from users.services import (describe_image_from_base64, get_image_vector_from_base64, get_image_vector_from_url, get_text_vector, get_cosine_similarity)
from image.services import get_images_from_db

class ImageViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def max_id(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLE STATUS LIKE 'image_image'")
            row = cursor.fetchone()
            auto_increment_value = row[10]
        return Response({'max_id': auto_increment_value})

    def get(self, request, *args, **kwargs):
        images = get_images_from_db(request.user.id)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    @action(detail=False, methods=['post'])
    def getImagesSimilarity(self, request, *args, **kwargs):
        try:
            getTextVector = get_text_vector(request.data.get("search"))

            imagesFromDb = get_images_from_db(request.user.id)
            
            imagesSearch = []
            mon_dictionnaire = {"images": None, "similarity": 0}

            for image in imagesFromDb:
                getImageVector = get_image_vector_from_base64(image.base64)
                getCosinusSimilarity = get_cosine_similarity(getImageVector, getTextVector)
                percentageSimilarity = getCosinusSimilarity * 100
                
                if(percentageSimilarity >= 20):
                    imageObject = {
                        "id": image.id,
                        "name": image.name,
                        "base64": image.base64,
                        "tags": image.tags,
                        "description": image.description,
                        "width": image.width,
                        "height": image.height,
                        "similarity": percentageSimilarity,
                    }

                    imagesSearch.append(imageObject)

            return Response(imagesSearch, status=status.HTTP_200_OK)

        except Exception as error:
           return Response({'msg': f'{error}'}, status=status.HTTP_400_BAD_REQUEST)
        

    def post(self, request):

        try:
            base64 = request.data.get("base64")
            
            cognitiveObjet = describe_image_from_base64(base64)

            wrongData = "Les informations saisies sont incorrectes."

            
            description = "" if cognitiveObjet.captions is None else cognitiveObjet.captions[0].text
            
            
            
            name = request.data.get('name')
            
            width = request.data.get('width')
            height = request.data.get('height')
            user = request.user.id

            tagsFromB64 = cognitiveObjet.tags
            print(tagsFromB64)
            # Authentification de l'utilisateur.
            image = {
                    'name': name,
                    'tags': ','.join(map(str, tagsFromB64)), #','.join(map(str, tagsFromB64.tags)),
                    'description': description,
                    'base64': base64,
                    'width' : width,
                    'height': height,
                    'user': user
                }
            
            serializer = ImageSerializer(data=image)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'msg': "L'image a correctement été créé."}, status=status.HTTP_200_OK)
            

        except Exception as error:
            return Response({'msg': f'{error}'}, status=status.HTTP_400_BAD_REQUEST)
        
    def custom_method(self, request):
        # Custom logic for the custom method
        images = Image.objects.filter(user = request.user.id)
        serializer = ImageSerializer(images, many=True)
        
        for img in serializer.data:
            print("serializer data")
            print(get_image_vector_from_base64(img['base64']))

        return Response("Custom method processed")
        

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