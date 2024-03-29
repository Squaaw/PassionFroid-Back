from django.contrib.auth.hashers import check_password, make_password
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import UserSerializer
from .utils import get_tokens_for_user, test_password, get_user_id_from_token, get_collection
from .models import User
from .services import *
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.


class UserViewSet(viewsets.ViewSet):
    def register(self, request):
        try:
            wrongData = "Les informations saisies sont incorrectes."
            email = request.data.get('email')
            password = request.data.get("password")

            if email is None or password is None:
                raise Exception(wrongData)

            # Looking for an existing account with the given email address before serialization to prevent exception since the email should be unique in the DB.
            if User.objects.filter(email=email):
                raise Exception('Adresse mail déjà utilisée.')

            if test_password(password) == False:
                raise Exception(
                    'Le mot de passe doit contenir au moins : 1 minuscule, 1 majuscule, 1 chiffre, 1 caractère spécial et 8 caractères minimum')

            user = {
                'email': email,
                'password': make_password(password)
            }

            serializer = UserSerializer(data=user)

            if serializer.is_valid():
                serializer.save()
                return Response({'msg': "L'utilisateur a correctement été créé."}, status=status.HTTP_200_OK)

            return Response({'msg': wrongData}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            return Response({'msg': f'{error}'}, status=status.HTTP_400_BAD_REQUEST)

    def login(self, request):
        try:
            email = request.data['email']
            password = request.data['password']

            try:
                user = User.objects.get(email=email)
            except:
                raise

            check = check_password(password, user.password)

            if check == False:
                raise

            auth_data = get_tokens_for_user(user)

            return Response({'msg': 'Authentification réussie !', **auth_data}, status=status.HTTP_200_OK)
        except:
            return Response({'msg': 'Identifiant ou mot de passe incorrect.'}, status=status.HTTP_401_UNAUTHORIZED)

    def saveImages(self, request):
        try:
            # Authentification de l'utilisateur.
            user_id = get_user_id_from_token(request)

            if user_id is None:
                return Response({'msg': 'La session a expirée.'}, status=status.HTTP_401_UNAUTHORIZED)

            # Récupération du produit.
            product = request.data.get('product')

            if product is None:
                return Response({'msg': 'Le champs product est requis.'}, status=status.HTTP_400_BAD_REQUEST)

            # Récupération de la collection "user".
            collection = get_collection("users_user")

            # Récupération des informations de l'utilisateur.
            user = collection.find_one({"id": user_id})

            if user is None:
                return Response({'msg': 'Utilisateur inconnu.'}, status=status.HTTP_401_UNAUTHORIZED)

            # Récupération de la liste des produits enregistrés.
            user_products = user.get('products')

            if user_products is None:
                # Création de la liste des produits si l'utilisateur enregistre un produit pour la première fois.
                collection.update_one(
                    {"id": user_id}, {'$set': {'products': [product]}})
            else:
                # Si l'utilisateur a déjà des produits enregistrés, on vérifie d'abord que le produit ne soit pas déjà enregistré afin d'éviter les doublons.
                if product in user_products:
                    return Response({'msg': 'Le produit figure déjà dans la liste des préférences.'}, status=status.HTTP_400_BAD_REQUEST)

                # Ajout du produit à la liste des produits enregistrés.
                collection.update_one(
                    {"id": user_id}, {'$push': {'products': product}})

            return Response({'msg': 'Le produit a été enregistré dans la liste des préférences.'}, status=status.HTTP_200_OK)

        except:
            return Response({'msg': settings.INTERNAL_ERROR_MESSAGE}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            # Authentification de l'utilisateur.
            user_id = get_user_id_from_token(request)

            if user_id is None:
                return Response({'msg': 'La session a expirée.'}, status=status.HTTP_401_UNAUTHORIZED)

            # Récupération du produit.
            product = request.data.get('product')

            if product is None:
                return Response({'msg': 'Le champs product est requis.'}, status=status.HTTP_400_BAD_REQUEST)

            # Récupération de la collection "user".
            collection = get_collection("users_user")

            # Récupération des informations de l'utilisateur.
            user = collection.find_one({"id": user_id})

            if user is None:
                return Response({'msg': 'Utilisateur inconnu.'}, status=status.HTTP_401_UNAUTHORIZED)

            # Récupération de la liste des produits enregistrés.
            user_products = user.get('products')

            if user_products is None or product not in user_products:
                return Response({'msg': 'Le produit ne figure pas dans la liste des préférences.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                # Suppression du produit enregistré.
                collection.update_one(
                    {"id": user_id}, {'$pull': {'products': product}})

            return Response({'msg': 'Le produit a été supprimé de la liste des préférences.'}, status=status.HTTP_200_OK)

        except:
            return Response({'msg': settings.INTERNAL_ERROR_MESSAGE}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def fetchImages(self, request):
        try:
            # Authentification de l'utilisateur.
            user_id = get_user_id_from_token(request)

            if user_id is None:
                return Response({'msg': 'La session a expirée.'}, status=status.HTTP_401_UNAUTHORIZED)

            # Récupération de la collection "user".
            collection = get_collection("users_user")

            # Récupération des informations de l'utilisateur.
            user = collection.find_one({"id": user_id})

            if user is None:
                return Response({'msg': 'Utilisateur inconnu.'}, status=status.HTTP_401_UNAUTHORIZED)

            # Récupération de la liste des produits enregistrés.
            user_images = user.get('images')

            if user_images is None or len(user_images) == 0:
                return Response({'msg': 'Aucun produit enregistré.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(user_images, status=status.HTTP_200_OK)

        except:
            return Response({'msg': settings.INTERNAL_ERROR_MESSAGE}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def generateImage(self, request):
        try:
            return HttpResponseRedirect(reverse("base_64_img", args=(image,)))
        except:
            return Response({'msg': "Une erreur interne est survenue lors de la génération de l'image."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
