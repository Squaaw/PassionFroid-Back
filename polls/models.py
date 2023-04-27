from django.db import models

# Create your models here.


class Image(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=400)
    tag = models.CharField(max_length=100)
    type = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    date_uploaded = models.DateTimeField(auto_now_add=True)


class User(models.Model):
    id_user = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    date_of_birth = models.DateField()
    role = models.CharField(max_length=20)


class Saleman(models.Model):
    id_saleman = models.IntegerField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE)


class Manager(models.Model):
    id_manager = models.IntegerField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
