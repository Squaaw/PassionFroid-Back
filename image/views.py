from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import connection
from django.db.models import Max
from rest_framework import status, viewsets
from .serializers import ImageSerializer
from .models import Image
from users.services import (describe_image_from_base64, get_image_vector_from_base64, get_text_vector, get_cosine_similarity)

class ImageViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def max_id(self, request):

        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLE STATUS LIKE 'image_image'")
            row = cursor.fetchone()
            auto_increment_value = row[10]  # L'indice 10 correspond à la colonne "Auto_increment"

        return Response({'max_id': auto_increment_value})

    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        images = Image.objects.filter(user = request.user.id)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            wrongData = "Les informations saisies sont incorrectes."

            name = request.data.get('name')
            tags = request.data.get('tags')
            description = request.data.get("description")
            base64 = request.data.get("base64")
            width = request.data.get('width')
            height = request.data.get('height')
            user = request.user.id

            tagsFromB64 = ["poisson,viande"] #describe_image_from_base64(base64.split(",")[1])
            
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