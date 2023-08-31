from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
# Create your models here.

def validate_unique_textfield(value):
    if Image.objects.filter(source=value).exists():
        raise ValidationError(('This value already exists.'))

class Image(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    source = models.TextField(blank=True, null=True, validators=[validate_unique_textfield])
    width = models.IntegerField(blank=True, null=False)
    height = models.IntegerField(blank=True , null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vector = models.JSONField(blank = True, null = False)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = False, null = False)

    def __str__(self):
        return self.name
