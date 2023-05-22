from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import ImageSerializer

class ImageViewSet(viewsets.ViewSet):
# Create your views here.
    def saveImages(self, request):
        try:
            wrongData = "Les informations saisies sont incorrectes."

            name = request.data.get('name')
            tags = request.data.get('tags')
            description = request.data.get("description")
            base64 = request.data.get("base64")
            # Authentification de l'utilisateur.
            image = {
                    'name': name,
                    'tags': tags,
                    'description': description,
                    'base64': base64,
                }
            print(image['name'])
            serializer = ImageSerializer(data=image)

            if serializer.is_valid(raise_exception=True):
                print("rrrrrrrrrrrrrrrrrrrrrrrrr")
                serializer.save()
                return Response({'msg': "L'image a correctement été créé."}, status=status.HTTP_200_OK)
            #return Response({'msg': wrongData}, status=status.HTTP_400_BAD_REQUEST)
            # user_id = get_user_id_from_token(request)

            # if user_id is None:
            #     return Response({'msg': 'La session a expirée.'}, status=status.HTTP_401_UNAUTHORIZED)

            # # Récupération du produit.
            # product = request.data.get('product')

            # if product is None:
            #     return Response({'msg': 'Le champs product est requis.'}, status=status.HTTP_400_BAD_REQUEST)

            # # Récupération de la collection "user".
            # collection = get_collection("users_user")

            # # Récupération des informations de l'utilisateur.
            # user = collection.find_one({"id": user_id})

            # if user is None:
            #     return Response({'msg': 'Utilisateur inconnu.'}, status=status.HTTP_401_UNAUTHORIZED)

            # # Récupération de la liste des produits enregistrés.
            # user_products = user.get('products')

            # if user_products is None:
            #     # Création de la liste des produits si l'utilisateur enregistre un produit pour la première fois.
            #     collection.update_one(
            #         {"id": user_id}, {'$set': {'products': [product]}})
            # else:
            #     # Si l'utilisateur a déjà des produits enregistrés, on vérifie d'abord que le produit ne soit pas déjà enregistré afin d'éviter les doublons.
            #     if product in user_products:
            #         return Response({'msg': 'Le produit figure déjà dans la liste des préférences.'}, status=status.HTTP_400_BAD_REQUEST)

            #     # Ajout du produit à la liste des produits enregistrés.
            #     collection.update_one(
            #         {"id": user_id}, {'$push': {'products': product}})

        except Exception as error:
            return Response({'msg': f'{error}'}, status=status.HTTP_400_BAD_REQUEST)